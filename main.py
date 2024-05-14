from datetime import datetime
from os import listdir
from os.path import join
from random import choice
from threading import Lock, Thread
from time import sleep as time_sleep

from numpy.linalg import norm
from sounddevice import play, wait, InputStream, sleep as sound_sleep
from soundfile import read

quiet_threshold = 20
loud_threshold = 40
quiet_loud_buffer_seconds = 0.5  # Account for loud sounds that tend to build gradually from quiet sounds.

input_device = 'Mic In (Elgato Wave:3), Windows WASAPI'
output_device = 'Wave Link SFX (Elgato Wave:3), MME'

quiet_directory = "quiet/"
loud_directory = "loud/"

quiet_files = [join(quiet_directory, f) for f in listdir(quiet_directory)]
loud_files = [join(loud_directory, f) for f in listdir(loud_directory)]

playing = False  # A flag to denote whether the sound is currently playing.
scheduled = False  # A flag to denote whether a quiet sound is scheduled to play after the delay.
lock = Lock()  # A lock for flags being used on multiple threads.


def delayed_execution(delay, f, args):
    def wait_and_execute():
        global scheduled
        time_sleep(delay)
        if scheduled:  # If a sound is scheduled, then play it.
            f(*args)
        scheduled = False  # Reset flag.

    Thread(target=wait_and_execute).start()


def play_sound(audio_file):
    global playing
    sound_data, fs = read(audio_file, dtype="float32")
    print(f"[{datetime.now()}] Playing '{audio_file}'")
    play(sound_data, fs, device=output_device)
    wait()  # Wait for the audio to finish before the next input.
    with lock:
        playing = False


def audio_callback(indata, _frames, _time, _status):
    global playing
    global scheduled

    with lock:
        if not playing:
            volume_norm = norm(indata) * 10

            if volume_norm > loud_threshold:
                scheduled = False
                audio_file = choice(loud_files)
                playing = True
                Thread(target=play_sound, args=(audio_file,)).start()

            elif volume_norm > quiet_threshold and not scheduled:
                audio_file = choice(quiet_files)
                scheduled = True
                playing = True
                delayed_execution(quiet_loud_buffer_seconds, play_sound, (audio_file,))


def exit_on_input(sound_stream):
    input()  # Waits until user presses enter.
    sound_stream.close()


now = datetime.now()
print(f"[{now}] Press Enter to exit")
print(f"[{now}] Listening to input device '{input_device}'")
print(f"[{now}] Playing sounds on output device '{output_device}'")

stream = InputStream(callback=audio_callback, device=input_device)

exit_thread = Thread(target=exit_on_input, args=(stream,), daemon=True)
exit_thread.start()

# Infinite loop to keep the stream running.
with stream:
    while stream.active:
        sound_sleep(1000)

print(f"[{datetime.now()}] Exiting...")
