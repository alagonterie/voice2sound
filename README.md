# Sound Triggered Audio Player in Python

A simple sound volume-triggered audio player written in Python. This script listens for audio through an input device and plays sound files from either a 'Quiet' or 'Loud' directory based on the detected volume level.

## Description

This script listens to an input audio stream and plays back preselected sound files based on the detected volume. If the volume level crosses a specified threshold, the script will play a random file from the corresponding directory:

- Files in the 'Quiet' directory are played when the volume level crosses the 'quiet' threshold.
- Files in the 'Loud' directory are played when the volume level crosses the 'loud' threshold.

## Requirements

- Python
- Installed packages: numpy, sounddevice, soundfile.
- Operating System: Windows

## Configuration

There are various parameters that you can adjust according to your requirements:

- `quiet_threshold`: The volume level above which 'quiet' sounds will be played.
- `loud_threshold`: The volume level above which 'loud' sounds will be played.
- `quiet_loud_buffer_seconds`: Delay in seconds to wait before deciding if the sound is just building up and to allow to switch to louder sound.
- `input_device`: The name of the audio input device.
- `output_device`: The name of the audio output device.
- `quiet_directory`: The path to the directory with 'quiet' sound files.
- `loud_directory`: The path to the directory with 'loud' sound files.

## How to Run

To execute the script, navigate to the directory containing `main.py` and run the following command:
`shell python main.py`

The script runs indefinitely, continuously monitoring the audio input stream. Press Enter to stop the script.

## Use Case

A livestream where the human vocal audio gets converted to random sound effects.
