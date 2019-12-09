import cv2
from threading import Thread
import imutils
import numpy as np
import datetime
import time
from threading import Thread
import cvlib
import random
from .utils import send_email, send_html_email


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.min_area = 300
        self.first_frame = None
        self.mean_delta_thresh = 100
        self.is_open = False

        _, self.frame = self.video.read()
        thread = Thread(target=self.update)
        thread.start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        self.is_open = True
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        self.is_open = False
        return jpeg.tobytes()

    def update(self):

        while True:
            while not self.is_open:
                pass

            _, self.frame = self.video.read()
            if self.frame is None:
                break

            # print("获取图片成功", time.time())
            # self.motion_detection()
            self.face_detection()
            if random.random() < 0.05:
                t = Thread(target=send_html_email, args=("Warning", "Someone invaded!", self.frame))
                t.start()

            cv2.putText(self.frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, self.frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    def face_detection(self):
        faces, confidences = cvlib.detect_face(self.frame)
        # loop through detected faces and add bounding box
        for face in faces:
            (startX, startY) = face[0], face[1]
            (endX, endY) = face[2], face[3]  # draw rectangle over face
            cv2.rectangle(self.frame, (startX, startY), (endX, endY), (0, 255, 0), 2)  # display output

    def motion_detection(self):
        text = "No motion"  # 还没有检测到人
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (31, 31), 0)  # 移除摄像头拍摄时的噪声

        # if the first frame is None, initialize it
        if self.first_frame is None:
            self.first_frame = gray
            return

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(self.first_frame, gray)
        thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]

        # 对阈值图像进行腐蚀, 把腐蚀区域的边缘变成2d box
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

        cnts = imutils.grab_contours(cnts)
        # loop over the contours
        for c in cnts:

            # if the contour is too small, ignore it
            if cv2.contourArea(c) < self.min_area:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            area = cv2.contourArea(c),
            delta_sum = np.sum(thresh[x: x + w, y: y + h])

            mean_delta = round(float(delta_sum / area), 2)
            if mean_delta < self.mean_delta_thresh:
                continue

            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(self.frame, "Average delta: {}".format(mean_delta), (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            text = "Occupied"

        # draw the text and timestamp on the frame
        cv2.putText(self.frame, "Room Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)