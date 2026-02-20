import sounddevice as sd
import queue
import json
import numpy as np
import scipy.signal
from vosk import Model, KaldiRecognizer
import core.flags

MODEL_PATH = "models/vosk-model-small-hi-0.22"
micRate = 48000
asrRate = 16000

_q = queue.Queue()
_textQueue = queue.Queue()

model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, asrRate)

def startListener():
    global stream

    stream = sd.RawInputStream(
        samplerate=micRate,
        blocksize=2000,
        dtype="int16",
        channels=1,
        callback=callBack
    )
    stream.start()


def stopMic():
    global stream
    if stream and stream.active:
        stream.stop()
        with _q.mutex:
            _q.queue.clear()

def startMic():
    global stream
    if stream and not stream.active:
        stream.start()

def pollMicText():

    while not _q.empty():

        data = _q.get()

        if core.flags.IS_SPEAKING.is_set():
            continue

        data_16k = resample(data)

        if rec.AcceptWaveform(data_16k):
            result = json.loads(rec.Result())
            text = result.get("text", "").strip()

            if text:
                _textQueue.put(text)

    if not _textQueue.empty():
        return _textQueue.get()

    return None

                

def callBack(indata, frames, time, status):
    _q.put(bytes(indata))


def resample(data: bytes) -> bytes:
    audio = np.frombuffer(data, dtype=np.int16)
    resampled = scipy.signal.resample(
        audio,
        int(len(audio) * asrRate / micRate)
    )
    return resampled.astype(np.int16).tobytes()
