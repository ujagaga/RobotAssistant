#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Listens to audio from microphone and waits for the configured wake word.
Once the wake word is detected, the program records audio and sends it to Google for converting to text.
When text is received, it is sent to an executor function which checks configured actions and triggers tha correct one
associated with this text command. The return message is then converted back to audio.
Currently, the file is prepared for use with Serbian language. All you need to do to use it with another language is to
change the "options.cfg" file which will be generated on first run.
"""

import os
import json
import random
import hashlib
import subprocess
import speech_recognition as sr
from gtts import gTTS


# Configuration
WAKE_WORD = "malecka"
LANG = 'sr'

WAKE_WORD_DIR = "wake_word"
RESPONSE_WORDS = ["molim", "da", "slušam", "kako mogu da pomognem", "izvolite", "recite"]
current_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(current_path, 'options.cfg')
audio_cache_dir = os.path.join(current_path, 'audio_samples')

# Prepare the wake word dir and listening command to execute
wake_word_path = os.path.join(current_path, WAKE_WORD_DIR, WAKE_WORD)
command = "arecord -r 16000 -f S16_LE -c 1 -t raw | rhasspy-wake-raven --average-templates --keyword {}" \
          "".format(wake_word_path)
actions_path = os.path.join(current_path, 'actions')
actions = []
sleep_process = None


def calc_hash(sentence):
    text_hash = hashlib.md5()
    text_hash.update(sentence.encode())
    return text_hash.hexdigest()


def text_to_audio(txt_data):
    audio_file_name = "{}.mp3".format(calc_hash(txt_data))
    audio_file_path = os.path.join(audio_cache_dir, audio_file_name)

    if not os.path.isfile(audio_file_path):
        speech = gTTS(text=txt_data, lang=LANG, slow=False)
        speech.save(audio_file_path)

    return audio_file_path


def select_response():
    # Choose randomly item from RESPONSE_WORDS list
    id = random.choice(range(0, len(RESPONSE_WORDS)))
    return RESPONSE_WORDS[id]


def generate_audio(text_to_say):
    if text_to_say is None:
        return
    hash_calculator = hashlib.md5()
    hash_calculator.update(text_to_say.encode())
    text_hash = hash_calculator.hexdigest()

    audio_file_name = "{}.mp3".format(text_hash)
    audio_file_path = os.path.join(audio_cache_dir, audio_file_name)

    if os.path.isfile(audio_file_path):
        print('Saying:', text_to_say)

    else:
        print('Generating:', text_to_say)
        text_to_audio(text_to_say)

    os.system("mpg321 {}".format(audio_file_path))


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, language=LANG)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def listen_user():
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Say something")

    guess = recognize_speech_from_mic(recognizer, microphone)

    if guess["transcription"] and guess["success"]:
        print("Heard:", guess["transcription"])
    else:
        print("ERROR:", guess["transcription"])

    return guess["transcription"]


# Listen to the user input
def sleep_listen():
    global sleep_process

    if sleep_process is None:
        sleep_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    # But do not wait till finish, start displaying output immediately
    try:
        while True:
            output = sleep_process.stdout.readline()
            if output == '' and sleep_process.poll() is not None:
                break
            if output:
                raw_data = output.decode().strip()
                try:
                    data = json.loads(raw_data)
                    print(data)
                    yield data

                except Exception as e:
                    print("ERR:", e)
    except:
        sleep_process.kill()
        print("EXITING")

    return None


def get_config():
    global WAKE_WORD
    global LANG
    global RESPONSE_WORDS

    # Read configuration from the cfg file if it exists
    if os.path.isfile(cfg_path):
        cfg = open(cfg_path, 'r')
        raw_data = cfg.read()
        cfg.close()
    else:
        raw_data = '{}'

    # Load the data info a json object
    try:
        data = json.loads(raw_data)
    except Exception as e:
        print('ERROR parsing config data: {}'.format(e))
        data = {}

    # Check if all data is available. If not, replace with defaults
    cfg_data_missing = False
    if 'WAKE_WORD' not in data.keys():
        data['WAKE_WORD'] = WAKE_WORD
        cfg_data_missing = True
    if 'LANG' not in data.keys():
        data['LANG'] = LANG
        cfg_data_missing = True
    if 'RESPONSE_WORDS' not in data.keys():
        data['RESPONSE_WORDS'] = RESPONSE_WORDS
        cfg_data_missing = True

    if cfg_data_missing:
        # Some of the configuration values are missing. Add them to the file.
        print("INFO: Writing new configuration.")

        # Custom data dump
        raw_data = "{\n"
        for key in data.keys():
            raw_data += '"{}": '.format(key)
            if isinstance(data[key], int) or isinstance(data[key], list):
                raw_data += '{},\n'.format(data[key])
            else:
                raw_data += '"{}",\n'.format(data[key])

        raw_data = raw_data[:-2] + '\n'
        raw_data += "}\n"

        raw_data = raw_data.replace("'", '"')

        try:
            cfg = open(cfg_path, 'w')
            cfg.write(raw_data)
            cfg.close()
        except Exception as e:
            print('ERROR writing configuration data: {}'.format(e))

    # Set defaults according to setup
    WAKE_WORD = data['WAKE_WORD']
    LANG = data['LANG']
    RESPONSE_WORDS = data['RESPONSE_WORDS']


def load_actions():
    global actions

    if not os.path.isdir(actions_path):
        os.path.mkdir(actions_path)

    dir_contents = os.listdir(actions_path)
    for item in dir_contents:
        # Check if item is a directory
        item_path = os.path.join(actions_path, item)
        if os.path.isdir(item_path):
            # Check if there is a "words" file and an "action" script
            words_path = os.path.join(item_path, "words")
            script_path = os.path.join(item_path, "action")
            if os.path.isfile(words_path) and os.path.isfile(script_path):
                if not os.access(script_path, os.X_OK):
                    print("Script {} is not executable. Making it so.".format(script_path))
                    os.chmod(script_path, 0o777)

                f = open(words_path, 'r')
                data = f.read().replace('\n', '')
                f.close()

                trigger_words = []
                for word in data.split(','):
                    trigger_words.append(word.strip())

                actions.append({'trig': trigger_words, 'exec': script_path})


def execute(command_string):
    print("EXEC:", command_string)
    matched_action = None

    try:
        for test_action in actions:
            words = test_action['trig']
            # Check if any of the words are in this action
            for test_word in command_string.split(' '):
                if test_word in words:
                    matched_action = test_action['exec']
                    command = [matched_action, command_string]
                    process = subprocess.run(command, check=True, stdout=subprocess.PIPE, universal_newlines=True)
                    output = process.stdout
                    return output
    except Exception as e:
        print("ERROR executing action:", e)
    return None


# Prepare audio cache directory
if not os.path.isdir(audio_cache_dir):
    os.mkdir(audio_cache_dir)

get_config()
load_actions()

while True:
    for result in sleep_listen():
        generate_audio(select_response())
        user_request = listen_user()
        if user_request is not None:
            # Execute the request
            response = execute(user_request)
            generate_audio(response)
