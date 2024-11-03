# Blinkit

## Overview

The **Blinkit** is a fun interactive game built using Python that tests your ability to keep your eyes open while your face is detected through a webcam. The game uses facial landmark detection to calculate the Eye Aspect Ratio (EAR) and tracks the player's score based on their ability to avoid blinking.

## Features

- Real-time face detection and blink tracking using the webcam.
- Engaging user interface built with CustomTkinter.
- Score tracking to challenge your friends and family.
- High score saving for tracking performance over time.
- Simple restart and quit functionality.

## Requirements

To run the game, you'll need to run the following command:

To install the required packages, run the following command:

```bash
pip install -r requirements.txt


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Fuad-san/Blinkit.git
   cd Blinkit
   ```
2. Create a virtual environment (recommended):
   ```bash
   Copy code
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game
   python Blinkit.py


## Controls

- **Start Game**: Click the "Start Game" button to begin.
- **Restart**: After the game ends, click the "Restart" button to play again.
- **Quit**: Click the "Quit" button to exit the game.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Any improvements or suggestions are welcome!

## License

This project is licensed under the MIT License .

## Acknowledgments

- [Dlib](http://dlib.net/) for the facial landmark detection.
- [OpenCV](https://opencv.org/) for real-time image processing.
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern user interface.

