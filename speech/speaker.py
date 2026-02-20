import subprocess
import os
import time
import queue
import threading
import speech.listener
import core
_speechQueue = queue.Queue()
_workerThread = None
_running = False


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PIPER_DIR = os.path.join(BASE_DIR, "models","piper")
PIPER_BIN = os.path.join(PIPER_DIR, "piper")
MODEL_PATH = "/home/vish/hindiAssistant/models/piper/hi_IN-rohan-medium.onnx"

_piper = None
_aplay = None

def initSpeaker():

    global _piper, _aplay

    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = PIPER_DIR + ":" + env.get("LD_LIBRARY_PATH", "")

    _piper = subprocess.Popen(
        [PIPER_BIN, "--model", MODEL_PATH, "--output_raw", "--interactive", "--threads", "2"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        env=env
    )
    time.sleep(3.0)

    _aplay = subprocess.Popen(
        ["aplay", "-D", "plughw:0,0","-B", "100000", "-F", "20000","-r", "22050", "-f", "S16_LE", "-t", "raw","-"],
        stdin=_piper.stdout
    )

    global _workerThread, _running

    _running = True
    _workerThread = threading.Thread(target=_audioWorker, daemon=True)
    _workerThread.start()

    speak(" \n")



def speak(text: str):
    
    global _piper

    if not text or not _piper:
        return

    text = text.replace('"', '').strip()
  
    _speechQueue.put(text)

def shutdownSpeaker():
    global _piper, _aplay, _speechQueue  , _workerThread, _running
    _running = False
    _speechQueue.put(None)
    if _workerThread:
        _workerThread.join()


    if _piper:
        _piper.terminate()
        _piper = None

    if _aplay:
        _aplay.terminate()
        _aplay = None

def _audioWorker():
    global _running, _piper
    print("Queue size:", _speechQueue.qsize())
    while _running:
        text = _speechQueue.get()

        if text is None:
            break

        core.flags.IS_SPEAKING.set()

        try:
            _piper.stdin.write((text + "\n").encode("utf-8"))
            _piper.stdin.flush()
            time.sleep(estimateDuration(text))
        except Exception as e:
            print("Audio worker error:", e)
            print("Piper return code:", _piper.poll())

        core.flags.IS_SPEAKING.clear()
        _speechQueue.task_done()


def estimateDuration(text):

    clean_text = text.replace(" ", "").replace(".", "").replace("?", "")
    char_count = len(clean_text)
    
    duration = (char_count * 0.18) + 1.8
    return duration









# def speak(text: str):

#     global _currentSpeech

#     if not text:
#         return

#     text = text.replace('"', '').strip()

#     env = os.environ.copy()
#     env["LD_LIBRARY_PATH"] = PIPER_DIR + ":" + env.get("LD_LIBRARY_PATH", "")

#     if _currentSpeech and _currentSpeech.poll() is None:
#         _currentSpeech.kill()

#     cmd = (
#         f'echo "{text}" | '
#         f'{PIPER_BIN} --model {MODEL_PATH} --output_raw | '
#         f'aplay -r 22050 -f S16_LE -t raw -'
#     )

#     _currentSpeech = subprocess.Popen(
#         cmd,
#         shell=True,
#         env=env
#     )


# def stopSpeech():

#     global _currentSpeech

#     if _currentSpeech and _currentSpeech.poll() is None:
#         _currentSpeech.kill()
#         _currentSpeech = None
