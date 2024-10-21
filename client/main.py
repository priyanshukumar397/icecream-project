import time
import subprocess
from gpiozero import Button

class ButtonHandler:
    def __init__(self):
        # Define the GPIO pins for the buttons
        self.orangeButton = Button(13)
        self.blackButton = Button(12)

        # Variables to hold the process objects
        self.orangeProcess = None
        self.blackProcess = None

        # Assign the event handlers to the buttons
        self.orangeButton.when_pressed = self.handleOrangePress
        self.blackButton.when_pressed = self.handleBlackPress

    def handleOrangePress(self):
        if self.orangeProcess is None:
            if self.blackProcess is None:
                # Start the orange script
                self.orangeProcess = subprocess.Popen(['/home/anant/main/venv/bin/python', '/home/anant/main/clientbot.py'])
                print("Started orange script.")
            else:
                print("Black script is running, ignoring orange button press.")
        else:
            # Terminate the orange script
            self.orangeProcess.terminate()
            self.orangeProcess.wait()
            self.orangeProcess = None
            print("Terminated orange script.")

    def handleBlackPress(self):
        if self.blackProcess is None:
            if self.orangeProcess is None:
                # Start the black script
                self.blackProcess = subprocess.Popen(['/home/anant/main/venv/bin/python', '/home/anant/main/notebot.py'])
                print("Started black script.")
            else:
                print("Orange script is running, ignoring black button press.")
        else:

            # Terminate the black script
            self.blackProcess.terminate()
            self.blackProcess.wait()
            self.blackProcess = None
            print("Terminated black script.")

    def run(self):
        try:
            while True:
                time.sleep(1)  # Sleep to prevent high CPU usage
        except KeyboardInterrupt:
            # Clean up on exit
            if self.orangeProcess is not None:
                self.orangeProcess.terminate()
                self.orangeProcess.wait()
            if self.blackProcess is not None:
                self.blackProcess.terminate()
                self.blackProcess.wait()
            print("Exiting program.")

if __name__ == "__main__":
    handler = ButtonHandler()
    handler.run()
