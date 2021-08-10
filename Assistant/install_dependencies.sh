#!/bin/bash

# Raven wake word dependencies
sudo apt install liblapack3 libatlas-base-dev
pip3 install rhasspy-wake-raven

# Recognition engine deps
sudo apt install mpg321
pip3 install PyAudio gTTS google-cloud-speech SpeechRecognition 

