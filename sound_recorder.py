import signal
import threading
import wave

import pyaudio

record = True


def key_listener():
    global record
    input()
    record = False


def startRecording():
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = "sample.wav"

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    t = threading.Thread(target=key_listener)
    t.start()

    while record:
        data = stream.read(CHUNK)
        frames.append(data)

    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def stopRecording(signum, frame):
    global record
    if signum == signal.SIGINT:
        print('Signal received')
        record = False


def record_audio():
    signal.signal(signal.SIGINT, stopRecording)
    startRecording()


if __name__ == '__main__':
    record_audio()
