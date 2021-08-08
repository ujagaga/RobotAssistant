# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2021 Martin Knoche
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import threading
import cv2
import time
from database import DatabaseHandler


class Camera:
    def __init__(self, stream_id=0, show_img=True):
        self.stream_id = stream_id
        self.currentFrame = None
        self.ret = False
        self.stop = False
        self.capture = cv2.VideoCapture(stream_id)
        self.thread = threading.Thread(target=self.update_frame)
        self.show_img = show_img

    # Continually updates the frame
    def update_frame(self):
        while True:
            self.ret, self.currentFrame = self.capture.read()
            while self.currentFrame is None:  # Continually grab frames until we get a good one
                self.capture.read()
            if self.stop:
                break

    # Get current frame
    def get_frame(self):
        return self.ret, self.currentFrame

    def screen(self, function):
        self.thread.start()
        window_name = "Streaming from {}".format(self.stream_id)

        if self.show_img:
            cv2.namedWindow(window_name)

        person_present_at = 0
        person_present_flag = False
        last = 0
        dbase = DatabaseHandler()
        while True:
            ret, frame = self.get_frame()
            if ret:
                frame, data = function(frame)
                fps = int(1 / (time.time() - last))
                data['fps'] = fps

                if self.show_img:
                    frame = cv2.putText(
                        frame,
                        "FPS:{}".format(fps),
                        (frame.shape[1] - 80, 30),
                        cv2.FONT_HERSHEY_PLAIN,
                        1,
                        (0, 255, 0),
                    )
                last = time.time()
                if self.show_img:
                    cv2.imshow(window_name, frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

                if 'name' in data.keys():
                    print(data)

                    dbase.update_face(data)
                    person_present_at = time.time()
                    person_present_flag = True
                else:
                    if (time.time() - person_present_at) > 2:
                        if person_present_flag:
                            print("Gone")
                        person_present_flag = False

        self.stop = True
        self.thread.join()
        if self.show_img:
            cv2.destroyWindow(window_name)
        self.capture.release()
        dbase.close()
