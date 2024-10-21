# icecream project

Icecream: the fastest way to build your voice-enabled AI hardware stack.

<img width="399" alt="Screenshot 2024-10-20 at 4 00 56 PM" src="https://github.com/user-attachments/assets/f7d5a91f-e7cd-44d8-976d-2ccabe5b8865">

## Overview

Icecream makes hardware one less thing to worry about by offering a seamless infrastructure for Conversational Al, allowing you to focus on what truly matters-creating a great user experience for your users.

Icecream comes prebuilt with firmware and hardware to build your conversational AI Device. Press the Home button to talk to a customizable voice assistant, Icecream also comes with a customizable button to trigger a custom action, this could be taking notes or giving you pro-active feedback as you go about your daily life or anything above and beyond.

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

## Acknowledgements

- Daily.co for video conferencing capabilities
- Pipecat for real-time communication
- The open-source community for various libraries and tools used in this project
