# Personal Assistant - malecka #

The python script "malecka.py" is using Rhasspy-wake-raven package to listen to user voice and detect the wake word.
Once the wake word is detected, the program records audio and sends it to Google for converting to text. 
The down side is lack of privacy and need for internet. The upside is that you can use any language supported by Google translate.
When text is received, it is sent to an executor function which checks configured actions and triggers the correct one
associated with this text command. The return message is then converted back to audio, also using Google services.
Currently, the file is prepared for use with Serbian language. All you need to do to use it with another language is to
change the "options.cfg" file which will be generated on first run.
It is intended for use on a linux/debian platform, but could easilly be adjusted for Windows or Mack.

## How to start? ##

Install dependencies:

    ./install_dependencies.sh

Run the script:

    puthon3 malecka.py
 

If you wish to use your custom wake word, run:

    python3 record_wake_word.py

The audio samples will be recorded in "wake_word" folder. After that you will need to use an audio editing software (like Audacity) to trim silence if any and normalize volume for better detection. You should record at least 5 samples of which you should select 3 you find best.

After that adjust the configuration file and restart the script.

## Aditional notes ##

Audio generating is using internet connection and can be a bit slow, but the audio files are cached in a subfolder, so a subsequent playing of the same text is faster.

## References ##

https://pypi.org/project/rhasspy-wake-raven/
https://pypi.org/project/gTTS/
https://pypi.org/project/SpeechRecognition/

## Contact ##

* [email me](ujagaga@gmail.com)






