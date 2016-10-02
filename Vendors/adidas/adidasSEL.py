from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from timeit import default_timer as timer
import re
import time

start = timer()

URL_home_url = "http://www.adidas.com/us/shoes"
URL_product_url = "http://www.adidas.com/us/pure-boost-x-shoes/BB4967.html"


driver = webdriver.Chrome(executable_path="./chromedriver")
#Execute get shoe homepage first for headers + cookie integrity
driver.get(URL_home_url)
driver.get(URL_product_url)

driver.find_element_by_xpath("//a[starts-with(@class, 'ui-dialog-titlebar-close')]").click()








end = timer()

print 'Runtime: ' + str(end - start)

