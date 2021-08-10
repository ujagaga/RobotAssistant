# Personal Assistant - malecka #

The python script "malecka.py" is using Mycroft-Precise wake engine to listen to user voice and detect the wake word.
Once the wake word is detected, the program records audio and sends it to Google for converting to text. 
The down side is lack of privacy and need for internet. The upside is that you can use any language supported by Google translate.
When text is received, it is sent to an executor function which checks configured actions and triggers the correct one
associated with this text command. The return message is then converted back to audio, also using Google services.
Currently, the file is prepared for use with Serbian language. All you need to do to use it with another language is to
change the "options.cfg" file which will be generated on first run.
It is intended for use on a linux/debian platform, but could easily be adjusted for Windows or Mack.

## How to start? ##

Install dependencies:

    ./install_dependencies.sh

Run the script:

    puthon3 malecka.py

## Aditional notes ##

Audio generating is using internet connection and can be a bit slow, but the audio files are cached in a subfolder, 
so a subsequent playing of the same text is faster.
Currently the wake word used is "hey-mycroft", but I intend to train my own custom word soon. 
You can also add your own wake word model in "wake_word" folder. Training your own model is described here:

    https://github.com/MycroftAI/mycroft-precise/wiki/Training-your-own-wake-word#how-to-train-your-own-wake-word

## References ##

    https://pypi.org/project/gTTS/
    https://pypi.org/project/SpeechRecognition/
    https://github.com/MycroftAI/mycroft-precise

## Contact ##

* [email me](ujagaga@gmail.com)






