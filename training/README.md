# Training Voice Recognition In Serbian Language #

The intention is to use Serbian Language without internet access. The English support will always be available.

To acomplish this, I need to add a serbian model to [VOSK API](https://alphacephei.com/vosk/). The AI training to produce the required model will be done using [Kaldi](https://kaldi-asr.org/doc/).

To build the serbian language model, I wrote a website to collect audio samples in serbian language: [audiosampler](https://audiosampler.herokuapp.com/).

If you need to collect samples in another language, the [website](https://github.com/ujagaga/audioSampler) is available for free and is easy to adjust for your another language.

A [free spoken digit dataset](https://github.com/Jakobovski/free-spoken-digit-dataset) is available in english. There are also a couple of scripts to split the audio samples as necessaary for the AI training.

