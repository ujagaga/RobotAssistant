#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess

WAKE_WORD = "wakeup"
WAKE_WORD_DIR = "wake_word"

current_path = os.path.dirname(os.path.realpath(__file__))
wake_word_path = os.path.join(current_path, WAKE_WORD_DIR, WAKE_WORD)
command = "arecord -r 16000 -f S16_LE -c 1 -t raw | rhasspy-wake-raven --record " + \
          wake_word_path + "'" + WAKE_WORD + "-{n:02d}.wav'"

print("Please record at least 5 samples and then review them, normalize, "
      "remove silence at start/end and keep just 3 of them.")
p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
(output, err) = p.communicate()
p_status = p.wait()
print(output)


