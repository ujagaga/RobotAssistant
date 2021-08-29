#!/bin/bash

arecord -D plughw:0,0 -d5 -f cd test.wav

