#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
from camera import Camera
from tools import FaceID
import os
import database


class Recognizer:
    def __init__(self, gal_dir=None, stream_id=0, show_img=True):
        # Initialization
        self.show_img = show_img
        self.cam = Camera(stream_id=stream_id, show_img=show_img)
        self.FaceID = FaceID(gal_dir=gal_dir)
        # Set OpenCV defaults
        self.color = (0, 0, 255)
        self.font = cv2.QT_FONT_NORMAL

    def annotate(self, img, results):
        out_data = {'img_w': len(img[0]), 'img_h': len(img)}

        for result in results:
            detections, ids = result

            (bbox, points, conf) = detections

            name, dist, id_conf = ids

            xc = int((bbox[1, 0] + bbox[0, 0])/2)
            yc = int((bbox[1, 1] + bbox[0, 1])/2)
            out_data['face_at_x'] = xc
            out_data['face_at_y'] = yc

            out_data['name'] = name
            out_data['conf'] = int(id_conf * 100)

            if self.show_img:
                # Draw name in the center
                img = cv2.putText(
                    img, "{}".format(name), (xc, yc), self.font, 0.7, (255, 255, 0)
                )

        return img, out_data

    def identification(self, frame):
        results = self.FaceID.recognize_faces(frame)
        frame, data = self.annotate(frame, results)
        return frame, data

    def run(self):
        self.cam.screen(self.identification)


current_path = os.path.dirname(os.path.realpath(__file__))
galleryPath = os.path.join(current_path, "FaceGallery", "sample_gallery")
Recognizer(gal_dir=galleryPath, show_img=True).run()


