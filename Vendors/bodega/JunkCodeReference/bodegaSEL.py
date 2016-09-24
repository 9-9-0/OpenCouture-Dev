from selenium import webdriver
from selenium.webdriver.support.ui import Select
from timeit import default_timer as timer
import re
import time
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
#driver = webdriver.Firefox(imageless_profile)
driver = webdriver.Firefox()
driver.get(URL_product_url)

#Select Shoe Size - Regex Steps:
#1) Strip whitespace
#2) Delete all text infront of the last "/"
#3) Get the text in front of the "-"
#Example string value: CHARCOAL / COREBLACK / VISTAGREY / 9.5 - $455.00

#Close the email subscription pop-up (this only occurs if you don't have cookies to disprove that you're a new visitor)
#Eventually get around to injecting cookies instead of doing this click
driver.find_element_by_xpath("//a[@class='close']").click()
#driver.implicitly_wait(10)


#Can this be shortened to one loop?
optionVal = ''

for element in driver.find_elements_by_xpath("//select[@id='product-select']/option"):
    size = re.sub('.* \/.', '', element.get_attribute("textContent"))
    size = re.sub('.-.*', '', size)
    if (size == user_size):
        print 'Size found: ' + size
        optionVal = element.get_attribute("value")
        print optionVal
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        #element.click()
        #driver.find_elements_by_xpath("//input[@id='add']").click()
        break

select = Select(driver.find_element_by_id('product-select'))
select.select_by_value(optionVal)

driver.find_elements_by_xpath("//input[@id='add']").click()


end = timer()
print "Runtime: " + str(end - start) + "s"
