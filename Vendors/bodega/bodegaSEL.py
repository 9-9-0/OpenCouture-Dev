from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from timeit import default_timer as timer
import re
import time
#NOTES:
# - NoSuchElementException for selenium error handling

def transformSizeToClass(size):
    if "." in size:
        output = re.sub('\.','-', size) + " available"
    else:
        output = size + " available"

    return output

URL_product_url = "https://shop.bdgastore.com/collections/footwear/products/y-3-qasa-boot"
URL_home_url = "https://shop.bdgastore.com/collections/footwear"
user_size = '10'
user_size = transformSizeToClass(user_size)
print 'User-Size Class Attribute Search Key: ' + user_size

start = timer()

#Set Up Profile, Eventually transition to complete headlessness
imageless_profile = webdriver.FirefoxProfile()
imageless_profile.set_preference('permissions.default.image', 2)
imageless_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

#Start the browser
#driver = webdriver.Firefox(imageless_profile)
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(URL_product_url)


### ADD TO CART ### (modularize this after script is complete)
#Close the email subscription pop-up (this only occurs if you don't have cookies to disprove that you're a new visitor)
#Eventually get around to injecting cookies instead of doing this click
driver.find_element_by_xpath("//a[@class='close']").click()
#driver.implicitly_wait(10)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

for li in driver.find_elements_by_xpath("//ul[@class='size options']/li"):
    if user_size in li.get_attribute("class"):
        li.click()

driver.find_element_by_xpath("//input[@id='add']").click()

#Quick little hack to make sure the add button executes before navigating to cart. 
#Look into various selenium wait functions to better handle this
time.sleep(.5)


### CHECKOUT ### (modularize this after script is complete)
driver.get('https://shop.bdgastore.com/cart')

'''
try:
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable(driver.find_elements_by_xpath("//input[@name='checkout']")))
except TimeoutException:
    print 'poop'
'''
time.sleep(.5)

driver.find_element_by_xpath("//input[@name='checkout']").click()








end = timer()
print "Runtime: " + str(end - start) + "s"
