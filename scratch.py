
# create cookies
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options, executable_path=r'C:\Utility\BrowserDrivers\chromedriver.exe')
driver.get('http://demo.guru99.com/test/cookie/selenium_aut.php')
driver.find_element(By.NAME, "username").send_keys("abc123")
driver.find_element(By.NAME, "password").send_keys("123xyz")
driver.find_element(By.NAME, "submit").click()
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

# retreive cookies
driver.get('http://demo.guru99.com/test/cookie/selenium_aut.php')
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get('http://demo.guru99.com/test/cookie/selenium_cookie.php')


# log in
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

elem = driver.find_element(By.NAME, "userLoginId")
elem.clear()
elem.send_keys("jakehazen70@gmail.com")
elem.send_keys(Keys.RETURN)
