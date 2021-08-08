# Face Recognition #

For now, I have face recognition via webcam working with writing data to a database. 

I used a face recognition software found on [this web page](https://pythonawesome.com/a-lightweight-face-recognition-toolbox-and-pipeline-based-on-tensorflow-lite/)

## How to start ##

1. Install dependencies.
You can easily install tflite-runtime from https://google-coral.github.io/py-repo/ with the following line:
pip3 install tflite-runtime --find-links https://google-coral.github.io/py-repo/tfli

2. Drop an image of you in FaceGallery/sample_gallery folder.
3. Run main_demo.py.

## Additional notes ##

In main_demo.py find line at the end:        
        
    Recognizer(gal_dir=galleryPath, show_img=True).run()

Here you can change show_img=False to remove video display. This should accelerate execution on slower computers. 

## Contact ##

* web: http://www.radinaradionica.com
* email: ujagaga@gmail.com

