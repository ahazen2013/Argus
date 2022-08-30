from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

SERVICES = ['https://www.netflix.com/SwitchProfile?tkn=GOCGTGD3QRF4LJNVYBKFVNOIEA', '']

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\Alex\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)
driver.get(SERVICES[0])
sleep(10)
driver.find_element(By.CLASS_NAME, 'watch-video').click()
sleep(10)
driver.find_element(By.CLASS_NAME, 'watch-video').click()
sleep(.5)
driver.find_element(By.CLASS_NAME, 'watch-video').click()
# assert "Netflix" in driver.title
# assert "No results found." not in driver.page_source
# driver.close()


