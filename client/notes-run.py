import os
import threading
import wave
import uuid
from cartesia import Cartesia
import pyaudio
from supabase import create_client, Client
import asyncio
import aiohttp
from dotenv import load_dotenv
import sys
import select
import tty
import termios

class VoiceRecorder:
    def __init__(self, cartesia_api_key, deepgram_api_key, supabase_url, supabase_key):
        self.cartesia_api_key = cartesia_api_key
        self.deepgram_api_key = deepgram_api_key
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.client = Cartesia(api_key=self.cartesia_api_key)
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
        self.model_id = "sonic-english"
        self.output_format = {
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 16000,
        }
        self.rate = 16000
        self.stop_recording = False

    def play_message(self, transcript):
        try:
            voice = self.client.voices.get(id=self.voice_id)
            p = pyaudio.PyAudio()
            stream = None

            for output in self.client.tts.sse(
                model_id=self.model_id,
                transcript=transcript,
                voice_embedding=voice["embedding"],
                stream=True,
                output_format=self.output_format,
            ):
                buffer = output["audio"]

                if not stream:
                    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=self.rate, output=True)

                stream.write(buffer)

            if stream is not None:
                stream.stop_stream()
                stream.close()
            p.terminate()

        except Exception as e:
            print(f"Error during message playback: {e}")
            return False
        return True

    def record_audio(self, filename):
        try:
            chunk = 1024
            sample_format = pyaudio.paInt16
            channels = 1
            fs = 44100

            p = pyaudio.PyAudio()
            stream = p.open(format=sample_format,
                            channels=channels,
                            rate=fs,
                            frames_per_buffer=chunk,
                            input=True)

            frames = []

            print("Recording... Press any key to stop.")

            def read_audio():
                while not self.stop_recording:
                    data = stream.read(chunk, exception_on_overflow=False)
                    frames.append(data)

            self.stop_recording = False
            t = threading.Thread(target=read_audio)
            t.start()

            # Save the terminal settings
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)

            try:
                # Set the terminal to raw mode
                tty.setcbreak(fd)
                while not self.stop_recording:
                    # Check if there is keyboard input
                    dr, dw, de = select.select([sys.stdin], [], [], 0)
                    if dr:
                        c = sys.stdin.read(1)
                        self.stop_recording = True
            finally:
                # Restore the terminal settings
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

            t.join()

            stream.stop_stream()
            stream.close()
            p.terminate()

            # Save as WAV
            wf = wave.open(filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()

            print(f"Recording saved to {filename}")
            return filename

        except Exception as e:
            print(f"Error during recording: {e}")
            return None

    async def transcribe_audio(self, file_path):
        try:
            deepgram_url = 'https://api.deepgram.com/v1/listen'

            headers = {
                'Authorization': f'Token {self.deepgram_api_key}',
                'Content-Type': 'audio/wav'
            }

            with open(file_path, 'rb') as audio_file:
                audio_data = audio_file.read()

            async with aiohttp.ClientSession() as session:
                async with session.post(deepgram_url, headers=headers, data=audio_data) as resp:
                    if resp.status != 200:
                        print(f"Error during transcription: {resp.status}")
                        return None
                    response = await resp.json()
                    transcription = response['results']['channels'][0]['alternatives'][0]['transcript']
                    print(f"Transcription: {transcription}")
                    return transcription

        except Exception as e:
            print(f"Error during transcription: {e}")
            return None

    def insert_transcription_into_db(self, transcription):
        try:
            # Generate a unique ID
            record_id = str(uuid.uuid4())

            # Prepare the data to insert
            data = {
                'id': record_id,
                'transcription': transcription
            }

            # Insert into Supabase table named 'transcriptions'
            res = self.supabase.table('transcriptions').insert(data).execute()

            # Check for errors in the response
            if res.error is not None:
                print(f"Error inserting into database: {res.error}")
                return False
            else:
                print(f"Transcription inserted into database with ID: {record_id}")
                print(f"Inserted data: {res.data}")
                return True
        except Exception as e:
            print(f"Exception occurred: {e}")
            return False

    def run(self):
        if self.play_message("Hey, please record your note"):
            wav_file = self.record_audio('output.wav')
            if wav_file:
                # Transcribe the audio
                transcription = asyncio.run(self.transcribe_audio(wav_file))
                if transcription is not None:
                    # Insert transcription into database
                    insert_success = self.insert_transcription_into_db(transcription)
                    if insert_success:
                        print("Transcription inserted into database successfully.")
                    else:
                        print("Failed to insert transcription into database.")
                else:
                    print("Transcription failed.")
            else:
                print("Recording failed.")
        else:
            print("Failed to play message.")

if __name__ == "__main__":
    load_dotenv(override=True)
    CARTESIA_API_KEY = os.environ.get('CARTESIA_API_KEY')
    DEEPGRAM_API_KEY = os.environ.get('DEEPGRAM_API_KEY')
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

    recorder = VoiceRecorder(CARTESIA_API_KEY, DEEPGRAM_API_KEY, SUPABASE_URL, SUPABASE_KEY)
    recorder.run()
