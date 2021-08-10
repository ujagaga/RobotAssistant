#!/bin/bash

# Raven wake word dependencies
sudo snap install mycroft-precise --edge
sudo apt install liblapack3 libatlas-base-dev mpg321
sudo pip3 install precise-runner
pip3 install PyAudio gTTS google-cloud-speech SpeechRecognition 

