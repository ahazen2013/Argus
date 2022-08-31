
#TODO:
# add other services (Hulu, HBO, Prime, D+)
# figure out what's up with the pause triple-click? (first manipulation after click with real mouse)
# have it look for my face specifically, and lower the threshold?
# doesn't work in the dark (obvi- look for a better camera or flood the room with IR light)
# remove LEDs from the camera? (should get a backup camera if we're doing this)

import cv2
import logging as log
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common import exceptions

SERVICES = ['https://www.netflix.com/SwitchProfile?tkn=GOCGTGD3QRF4LJNVYBKFVNOIEA',
            'https://play.hbomax.com/page/urn:hbo:page:home']   # HBO: login info not stored, video element not there

# gives facial recognition a pattern to look for
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
# log.basicConfig(filename='webcam.log', level=log.INFO)

video_capture = cv2.VideoCapture(0)
present = True

options = webdriver.ChromeOptions()
# load Chrome profile, so it isn't using an empty guest profile
options.add_argument("user-data-dir=C:\\Users\\Alex\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
options.add_argument("start-maximized")
# get rid of the annoying notification that Chrome is being controlled by an automated process
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
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
    # if the last person just left the webcam's view, or the first person just entered it
    if len(faces) ^ present:
        sleep(.5)
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # make sure it wasn't just a momentary absence/presence
        # (this is to prevent unwanted pauses mostly)
        if len(faces) ^ present:
            # pause/resume the video
            try:
                driver.find_element(By.CLASS_NAME, 'watch-video').click()
                sleep(0.5)
                driver.find_element(By.CLASS_NAME, 'watch-video').click()
                present = not present
                # netflix takes 2 seconds to reduce the play bar: .5 + 1.25 + .25 = 2
                sleep(1.25)
            # make sure the program doesn't crash if we're not currently watching Netflix
            except exceptions.NoSuchElementException:
                pass
    # checks for faces four times a second instead of continuously, to conserve resources
    sleep(.25)

    # log.info("faces: " + str(len(faces)) + " at " + str(dt.datetime.now()))

# label=driver.find_element(By.XPATH,'/div/div[2]/div/div/div[3]/div/div[1]/div[1]/button').get_attribute('aria-label')
# driver.find_element(By.CLASS_NAME, 'playback-notification playback-notification--play').click()
# class: active ltr-omkt8s/inactive ltr-omkt8s
# When everything is done, release the capture
# class: active ltr-omkt8s/inactive ltr-omkt8s
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()


