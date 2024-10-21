# Icecream: The Fastest way to build your voice-enabled AI hardware stack.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)&ensp;&ensp;&ensp;

<img width="399" alt="Screenshot 2024-10-20 at 4 00 56 PM" src="https://github.com/user-attachments/assets/6f7721d9-0acc-4bef-bcc8-e4d8ae0b6ca7">



## Overview

Icecream makes hardware one less thing to worry about by offering a seamless infrastructure for Conversational Al, Icecream comes prebuilt with firmware and hardware to build your conversational AI Device. Press the Home button to talk to a customizable voice assistant, Icecream also comes with a customizable button to trigger a custom action, this could be taking notes or giving you pro-active feedback as you go about your daily life or anything above and beyond.

## Key Features

- AI-driven conversational abilities powered by LLMs
- Real-time voice input and output using Pipecat and Daily
- Seamless video conferencing integration via Daily.co
- Persistent conversation logging and retrieval

## Technical Stack

- Backend: Python with FastAPI
- AI Model: Custom choice of models
- Real-time Communication: Pipecat and Daily
- Speech Processing: PyAudio
- Video Conferencing: Daily.co API
- Database: Supabase

## Hardware
- Raspi Zero
- Keyestudio 5V ReSpeaker 2-Mic Pi HAT V1.0 Expansion Board For Raspberry Pi 4B +CE Compliant W/B+/3B+/3B
- Raspberry Pi Zero 2 W (with Quad-core CPU,Bluetooth 4.2,BLE,onboard Antenna,etc.)
- Stereo 8 Ohm Speakers
- 3D Printed Case

## Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-interactive-chatbot.git
   cd ai-interactive-chatbot
   ```

2. Set up the environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure your environment:
   ```
   cp env.example .env
   # Edit .env with your API keys and configurations
   ```

4. Launch the application:
   ```
   python server.py
   ```

5. Access the chatbot interface at `http://localhost:7860/start`

## Project Structure

- `server.py`: Main application server
- `bot.py`: Core chatbot logic
- `client/`: Client-side scripts
  - `pyaudio-run.py`: Voice interaction handler
  - `notes-run.py`: Conversation logging system
  - `main.py`: Main python script
- `requirements.txt`: Python dependencies

## Community and Support

If you have any questions, need assistance with setup, or want to contribute to the project, join the [Open Vision Engineering](https://discord.gg/j6a4dxjc) community. You'll find helpful resources, a welcoming community, and a contribution guide to get you started.

## License

All projects under Open Vision Engineering are released under the MIT License, allowing for open collaboration and innovation.

