from selenium import webdriver
from timeit import default_timer as timer
import re
#NOTES:
# - NoSuchElementException for selenium error handling

URL_product_url = "https://shop.bdgastore.com/collections/footwear/products/y-3-qasa-boot"
URL_home_url = "https://shop.bdgastore.com/collections/footwear"
user_size = '10'

start = timer()

#Set Up Profile, Eventually transition to complete headlessness
imageless_profile = webdriver.FirefoxProfile()
imageless_profile.set_preference('permissions.default.image', 2)
imageless_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

#Start the browser
driver = webdriver.Firefox(imageless_profile)
driver.get(URL_product_url)

#Select Shoe Size - Regex Steps:
#1) Strip whitespace
#2) Delete all text infront of the last "/"
#3) Get the text in front of the "-"
#Example string value: CHARCOAL / COREBLACK / VISTAGREY / 9.5 - $455.00

#Can this be shortened?
#selectElem = driver.find_element_by_xpath("//select[@id='product-select']")
#options = [x for x in selectElem.find_elements_by_tag_name("option")]
#for element in options:
#    print element.getText()
for element in driver.find_elements_by_xpath("//select[@id='product-select']/option"):
    print element.text



end = timer()
print "Runtime: " + str(end - start) + "s"
