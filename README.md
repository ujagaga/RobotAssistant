# Face And Voice Recognition Smart Robot #

This is my first robot. It is still in development. For now, I have:
- face recognition via webcam working with writing data to a database
- prepared Rhaspy speach recognition toolkit
- 3D model of the casing with two servo motors to house the computer with microphone, webcam,..

My goal is to build a robot with servos using Orange Pi Zero, to follow the detected persons face, recognize voice commands and execute them. 

I used a face recognition software found on [this web page](https://pythonawesome.com/a-lightweight-face-recognition-toolbox-and-pipeline-based-on-tensorflow-lite/)

The speach recognition and voice assistant fetures come from [Rhasspy](https://rhasspy.readthedocs.io/en/latest/)

## How to start ##

1. Prepare an Orange Pi Zero (or Raspberry Pi 2+ or any other similar or better single board computer) with a linux server environment, microphone, camera and GPIO pins available

2. Install dependencies.
For face recognition, you can install Tensor Flow Lite from https://google-coral.github.io/py-repo/ with the following line:

        pip3 install tflite-runtime --find-links https://google-coral.github.io/py-repo/tfli

3. Drop an image of you in FaceRecognition/FaceGallery/sample_gallery 

4. Run FaceRecognition/main_demo.py to test the face recognition software

5. Stay tuned for further updates :D

## Additional notes ##

In main_demo.py find line at the end:        
        
    Recognizer(gal_dir=galleryPath, show_img=True).run()

Here you can change show_img=False to remove video display. This should accelerate execution on slower computers. 

## Contact ##

* web: http://www.radinaradionica.com
* email: ujagaga@gmail.com

