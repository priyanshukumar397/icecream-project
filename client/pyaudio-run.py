#
# Copyright (c) 2024, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import threading
import time
import requests
import pyaudio
import daily
import json

SAMPLE_RATE = 16000
NUM_CHANNELS = 1
CHUNK_SIZE = 640

class PyAudioApp(daily.EventHandler):
    def __init__(self, sample_rate, num_channels):
        super().__init__()
        self.__app_quit = False
        self.__app_error = None
        self.__app_joined = False
        self.__app_inputs_updated = False
        self.__num_channels = num_channels

        self.__start_event = threading.Event()

        # Configure microphone and speaker devices with matching parameters
        self.__virtual_mic = daily.Daily.create_microphone_device(
            "my-mic",
            sample_rate=sample_rate,
            channels=num_channels
        )

        self.__virtual_speaker = daily.Daily.create_speaker_device(
            "my-speaker",
            sample_rate=sample_rate,
            channels=num_channels
        )
        daily.Daily.select_speaker_device("my-speaker")

        # PyAudio setup
        self.__pyaudio = pyaudio.PyAudio()

        # Input stream (microphone)
        self.__input_stream = self.__pyaudio.open(
            format=pyaudio.paInt16,
            channels=num_channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=CHUNK_SIZE
        )

        # Output stream (speaker)
        self.__output_stream = self.__pyaudio.open(
            format=pyaudio.paInt16,
            channels=num_channels,
            rate=sample_rate,
            output=True,
            frames_per_buffer=CHUNK_SIZE
        )

        self.__client = daily.CallClient(event_handler=self)

        self.__client.update_inputs({
            "camera": False,
            "microphone": {
                "isEnabled": True,
                "settings": {
                    "deviceId": "my-mic",
                    "customConstraints": {
                        "autoGainControl": {"exact": True},
                        "noiseSuppression": {"exact": True},
                        "echoCancellation": {"exact": True},
                    }
                }
            }
        })

        self.__client.update_subscription_profiles({
            "base": {
                "camera": "unsubscribed",
                "microphone": "subscribed"
            }
        })

        self.__participants = dict(self.__client.participants())
        del self.__participants["local"]

        # Start threads for audio processing
        self.__send_user_audio_thread = threading.Thread(target=self.send_user_audio)
        self.__receive_bot_audio_thread = threading.Thread(target=self.receive_bot_audio)

        self.__send_user_audio_thread.start()
        self.__receive_bot_audio_thread.start()

    def on_inputs_updated(self, inputs):
        self.__app_inputs_updated = True
        self.maybe_start()

    def on_joined(self, data, error):
        if error:
            print(f"Unable to join call: {error}")
            self.__app_error = error
        else:
            self.__app_joined = True
            print("Joined call!")
        self.maybe_start()
    
    def on_participant_left(self, participant, reason):
        if len(self.client.participants()) < 2:
            self.logger.info("participant left")
            self.client.leave()

    def maybe_start(self):
        if self.__app_error:
            self.__start_event.set()

        if self.__app_inputs_updated and self.__app_joined:
            self.__start_event.set()

    def send_user_audio(self):
        self.__start_event.wait()

        if self.__app_error:
            print("Unable to send user audio due to error.")
            return

        while not self.__app_quit:
            try:
                buffer = self.__input_stream.read(
                    CHUNK_SIZE, exception_on_overflow=False)
                if len(buffer) > 0:
                    self.__virtual_mic.write_frames(buffer)
            except Exception as e:
                print(f"Error sending user audio: {e}")

    def receive_bot_audio(self):
        self.__start_event.wait()

        if self.__app_error:
            print("Unable to receive bot audio due to error.")
            return

        while not self.__app_quit:
            buffer = self.__virtual_speaker.read_frames(CHUNK_SIZE)
            if len(buffer) > 0:
                try:
                    self.__output_stream.write(buffer)
                except Exception as e:
                    print(f"Error receiving bot audio: {e}")

    def run(self, meeting_url):
        self.__client.join(meeting_url, completion=self.on_joined)
        # Wait for threads to finish
        self.__send_user_audio_thread.join()
        self.__receive_bot_audio_thread.join()

    def leave(self):
        self.__app_quit = True
        self.__client.leave()
        self.__client.release()
        self.__input_stream.close()
        self.__output_stream.close()
        self.__pyaudio.terminate()

def main():
    url = start_agent()
    print(url)
    daily.Daily.init()

    app = PyAudioApp(SAMPLE_RATE, NUM_CHANNELS)

    try:
        app.run(url)
    except KeyboardInterrupt:
        print("Ctrl-C detected. Exiting!")
    finally:
        app.leave()

def start_agent():
    url = "https://icecream.ngrok.app/start"
    headers = {
        "ngrok-skip-browser-warning": "true"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("Agent started successfully.")
        print("Redirect URL:", response.url)
        return response.url
    except requests.exceptions.RequestException as e:
        print(f"Failed to start agent: {e}")

if __name__ == '__main__':
    main()
