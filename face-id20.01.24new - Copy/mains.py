from dbfaces import *
from flask import Flask, render_template, request


app = Flask(__name__)
cam = cv2.VideoCapture(0)

face_from_video("D:\python\face-id20.01.24new\recorded-video.mp4",id)