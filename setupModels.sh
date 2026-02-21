#!/bin/bash

echo "Starting Model Download for Hindi Assistant..."

# 1. Download and Extract Vosk Model
echo "--- Downloading Vosk STT Model (Hindi) ---"
mkdir -p models
wget https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip
unzip vosk-model-small-hi-0.22.zip -d models/
rm vosk-model-small-hi-0.22.zip

# 2. Download and Extract Piper Engine (Raspberry Pi 64-bit architecture)
echo "--- Downloading Piper TTS Engine ---"
# Note: If using a 32-bit Pi OS, change 'aarch64' to 'armv7le'
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_aarch64.tar.gz
tar -xzf piper_linux_aarch64.tar.gz -C models/
rm piper_linux_aarch64.tar.gz

# 3. Download the Rohan Hindi Voice Model
echo "--- Downloading Rohan Hindi Voice ---"
# We put these inside the newly extracted models/piper/ folder
wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx -P models/piper/
wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx.json -P models/piper/

echo "All models and engines downloaded successfully!"
