
#TODO:
# add other services (Hulu, HBO, Prime, D+)
# add a delay (if no face for 1 sec)?
# have it look for my face, and lower the threshold?
# figure out what's up with the pause triple-click?
# add drivers to main file?

import cv2
import logging as log
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

SERVICES = ['https://www.netflix.com/SwitchProfile?tkn=GOCGTGD3QRF4LJNVYBKFVNOIEA', '']

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log', level=log.INFO)

video_capture = cv2.VideoCapture(0)
present = True

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\Alex\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)
driver.get(SERVICES[0])

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces):  # resume
        if not present:
            driver.find_element(By.CLASS_NAME, 'watch-video').click()
            sleep(0.5)
            driver.find_element(By.CLASS_NAME, 'watch-video').click()
            present = True
            sleep(2)

    else:           # pause
        if present:
            driver.find_element(By.CLASS_NAME, 'watch-video').click()
            sleep(0.5)
            driver.find_element(By.CLASS_NAME, 'watch-video').click()
            present = False
            sleep(2)

    log.info("faces: " + str(len(faces)) + " at " + str(dt.datetime.now()))


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()