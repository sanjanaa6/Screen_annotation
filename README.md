# Screen Annotation

A Python-based finger tracking project that captures webcam input and draws on a digital canvas based on your finger movement.

## Features

- Detects a single hand using the webcam
- Tracks the index finger tip position
- Draws strokes on a virtual overlay when your index finger is up
- Uses simple gesture controls:
  - Index finger up: draw
  - Index + middle finger up: pause
  - All fingers up: clear the canvas

## Requirements

- Python 3.8+
- `opencv-python`
- `mediapipe==0.9.1.0`

## Setup

1. Open a terminal in this folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python screen_annotation.py
```

## Usage

- Point your index finger toward the camera.
- Move your finger to draw on the screen.
- Raise your middle finger together with your index finger to pause drawing.
- Raise all fingers to clear the canvas.
- Press `q` or `Esc` to exit.
