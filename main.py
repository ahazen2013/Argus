
# TODO: add other services (Hulu, HBO, D+) (sign in, and look for other video elements)
# TODO: clean this place up!
# TODO: have it look for my face specifically, and lower the threshold?
# TODO: doesn't work in the dark (obvi- look for a better camera or flood the room with IR light)
# TODO: remove LEDs from the camera? (should get a backup camera if we're doing this)

import cv2
from selenium import webdriver
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common import exceptions
from argparse import ArgumentParser

SERVICES = ['https://www.netflix.com/SwitchProfile?tkn=GOCGTGD3QRF4LJNVYBKFVNOIEA',
            'https://play.hbomax.com/page/urn:hbo:page:home',
            'https://www.amazon.com/Amazon-Video/b/?ie=UTF8&node=2858778011&ref_=nav_cs_prime_video']
VIDEO_ELEMENTS = ['watch-video', 'HBO', 'f45h']

parser = ArgumentParser()
parser.add_argument('command', type=str)
args = parser.parse_args()
index = 0
if args.command == 'netflix':
    index = 0
if args.command == 'hbo':
    index = 1
elif args.command == 'amazon':
    index = 2

# gives facial recognition a pattern to look for (front-facing face or profile of a face)
frontCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
profileCascade = cv2.CascadeClassifier("haarcascade_profileface.xml")

video_capture = cv2.VideoCapture(0)
present = True
past = False

options = webdriver.ChromeOptions()
# load Chrome profile, so it isn't using an empty guest profile
options.add_argument("user-data-dir=C:\\Users\\Alex\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
options.add_argument("start-maximized")
# get rid of the annoying notification that Chrome is being controlled by an automated process
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
driver.get(SERVICES[index])

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    front = frontCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    left = profileCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    right = profileCascade.detectMultiScale(
        cv2.flip(gray, 1),
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    f = bool(len(front) or len(left) or len(right))  # looks at front, left profile, and right profile
    # if the last person just left the webcam's view, or the first person just entered it
    if (f == past) and (f != present):
        try:
            action = ActionBuilder(driver)
            action.pointer_action.move_to_location(8, 0)
            action.perform()
            if index == 2:
                buttons = driver.find_elements(By.CLASS_NAME, VIDEO_ELEMENTS[index])
                buttons[2].click()
            else:
                driver.find_element(By.CLASS_NAME, VIDEO_ELEMENTS[index]).click()
            present = not present
        # make sure the program doesn't crash if we're not currently watching Netflix
        except exceptions.NoSuchElementException:
            pass
        sleep(1)
    elif f != past:
        sleep(.75)
    # checks for faces four times a second instead of continuously, to conserve resources
    past = f
    sleep(0.25)

# When everything is done, release the capture
video_capture.release()
