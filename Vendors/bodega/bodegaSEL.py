from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from timeit import default_timer as timer
import re
import time
import threading
#NOTES:
# - NoSuchElementException for selenium error handling

def transformSizeToClassAttr(size):
    if "." in size:
        output = re.sub('\.','-', size) + " available"
    else:
        output = size + " available"

    return output

#Eventually let this function call find_element() instead of find_element_by_id()
def attemptInput(by, key, value, maxAttempts):
#def attemptInput(value, idKey, maxAttempts):
    result = False
    attempts = 0
    while (attempts < maxAttempts):
        try:
            driver.find_element(by, key).send_keys(value)
            result = True
            break
        except StaleElementReferenceException:
            attempts = attempts + 1
    return result
'''
    result = False
    attempts = 0
    while (attempts < maxAttempts):
        try:
            driver.find_element_by_id(idKey).send_keys(value)
            result = True
            break
        except StaleElementReferenceException:
            attempts = attempts + 1
    return result
'''
#Script Configurations
#Eventually have these be imported from a file

URL_product_url = "https://shop.bdgastore.com/collections/footwear/products/y-3-qasa-boot"
URL_home_url = "https://shop.bdgastore.com/collections/footwear"
user_size = '10'
user_size = transformSizeToClassAttr(user_size)
#print 'User-Size Class Attribute Search Key: ' + user_size
email           = 'foo@gmail.com'
ship_phone      = '2122229393'
ship_first_name = 'Bob'
ship_last_name  = 'McyFlymo'
ship_company    = 'AyyLmao'
ship_address1   = '2999 5th Ave'
ship_address2   = 'Apt C'
ship_city       = 'Seattle'
ship_country    = 'United States'
ship_state      = 'Washington'
ship_zip        = '98101'
cc_num          = '4049379889248814'
cc_name         = 'Bob McFlymo'
cc_expiry       = '0318'
cc_cvv          = '233'
bill_first_name = 'Bob'
bill_last_name  = 'McFlymo'
bill_company    = 'AyyLmao'
bill_address1   = '2999 5th Ave'
bill_address2   = 'Apt C'
bill_city       = 'Seattle'
bill_country    = 'United States'
bill_state      = 'Washington'
bill_zip        = '98101'
bill_phone      = '2122229393'

start = timer()

#Set Up Profile, Eventually transition to complete headlessness
#imageless_profile = webdriver.FirefoxProfile()
#imageless_profile.set_preference('permissions.default.image', 2)
#imageless_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

#Start the browser
#driver = webdriver.Firefox(imageless_profile)
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(URL_product_url)

### ADD TO CART ### (modularize this after script is complete)
#Close the email subscription pop-up (this only occurs if you don't have cookies to disprove that you're a new visitor)
#Eventually get around to injecting cookies instead of doing this click?
driver.find_element_by_xpath("//a[@class='close']").click()

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#Get rid of xpath if possible, find a way to search for class names that contain spaces
try:
    WebDriverWait(driver,.1).until(EC.element_to_be_clickable((By.XPATH, "//ul[starts-with(@class, 'size options')]/li")))
except TimeoutException:
    print 'TIMEOUT ITEM SELECT'

for li in driver.find_elements_by_xpath("//ul[@class='size options']/li"):
    if user_size in li.get_attribute("class"):
        li.click()

driver.find_element_by_id("add").click()

#Not sure how to eliminate this sleep step, item gets added a few second fractions after the pop-up occurs, but waiting for the
#pop-up element to become stale takes way too long
#NOTE: Item gets added to cart BEFORE the javascript runs to modify the cart item quantity, for now time.sleep will have to suffice
'''
print driver.find_element_by_xpath("//a[starts-with(@class, 'hidden-lg open-cart cartcount')]").text
try:
    WebDriverWait(driver,1).until(EC.text_to_be_present_in_element((By.XPATH, "//a[starts-with(@class, 'hidden-lg open-cart cartcount')]"), '1'))
except TimeoutException:
    print 'TIMEOUT CART QUANTITY'
'''
time.sleep(.25)

### CHECKOUT ### (modularize this after script is complete)
driver.get('https://shop.bdgastore.com/cart')

try:
    WebDriverWait(driver,.25).until(EC.element_to_be_clickable((By.NAME, "checkout")))
except TimeoutException:
    print 'TIMEOUT CHECKOUT BUTTON'

#See if you can call the By/find_element only once. Issues with the EC.function() arguments when passing the webelement type through
driver.find_element_by_name("checkout").click()

### Begin filling out shipping form fields
driver.find_element_by_id("checkout_email").send_keys(email)
driver.find_element_by_id("checkout_shipping_address_first_name").send_keys(ship_first_name)
driver.find_element_by_id("checkout_shipping_address_last_name").send_keys(ship_last_name)
driver.find_element_by_id("checkout_shipping_address_company").send_keys(ship_company)
driver.find_element_by_id("checkout_shipping_address_address1").send_keys(ship_address1)
driver.find_element_by_id("checkout_shipping_address_address2").send_keys(ship_address2)
driver.find_element_by_id("checkout_shipping_address_city").send_keys(ship_city)

Select(driver.find_element_by_id("checkout_shipping_address_country")).select_by_visible_text(ship_country)
#This pause is for the state dropdown select to display. Again, need to switch over to Selenium's wait functionality
try:
    WebDriverWait(driver,.1).until(EC.element_to_be_clickable((By.ID, "checkout_shipping_address_province")))
except TimeoutException:
    print 'TIMEOUT STATE DROPDOWN'

Select(driver.find_element_by_id("checkout_shipping_address_province")).select_by_visible_text(ship_state)

driver.find_element_by_id("checkout_shipping_address_zip").send_keys(ship_zip)
driver.find_element_by_id("checkout_shipping_address_phone").send_keys(ship_phone)

driver.find_element_by_name("button").click()

#Select Shipping Method
#NOTE: Current case supported: Default shipping method already checked by default
driver.find_element_by_name("button").click()

#Input CC Info and Finalize
#NOTE: Current case supported: CC Payment with billing address that differs from shipping address
#NOTE: Issue with entering CC num, class of input element changes based on first 4 digits and thus, the element becomes stale

#Input CC num
num_iframe = driver.find_element_by_xpath("//iframe[starts-with(@name, 'card-fields-number')]")
driver.switch_to_frame(num_iframe)
for digit in cc_num:
    attemptInput(By.ID, "number", digit, 5)
    #attemptInput(digit, "number", 5)
driver.switch_to_default_content()

#Input CC name
name_iframe = driver.find_element_by_xpath("//iframe[starts-with(@name, 'card-fields-name')]")
driver.switch_to_frame(name_iframe)
driver.find_element_by_id("name").send_keys(cc_name)
driver.switch_to_default_content()

#Input CC expiry
expiry_iframe = driver.find_element_by_xpath("//iframe[starts-with(@name, 'card-fields-expiry')]")
driver.switch_to_frame(expiry_iframe)
for digit in cc_expiry:
    attemptInput(By.ID, "expiry", digit, 5)
#driver.find_element_by_id("expiry").send_keys(cc_expiry)
driver.switch_to_default_content()

#Input CC cvv
cvv_iframe = driver.find_element_by_xpath("//iframe[starts-with(@name, 'card-fields-verification')]")
driver.switch_to_frame(cvv_iframe)
driver.find_element_by_id("verification_value").send_keys(cc_cvv)
driver.switch_to_default_content()

#Input Billing Address
driver.find_element_by_id("checkout_billing_address_first_name").send_keys(bill_first_name)
driver.find_element_by_id("checkout_billing_address_last_name").send_keys(bill_last_name)
driver.find_element_by_id("checkout_billing_address_company").send_keys(bill_company)
driver.find_element_by_id("checkout_billing_address_address1").send_keys(bill_address1)
driver.find_element_by_id("checkout_billing_address_address2").send_keys(bill_address2)
driver.find_element_by_id("checkout_billing_address_city").send_keys(bill_city)

Select(driver.find_element_by_id("checkout_billing_address_country")).select_by_visible_text(bill_country)
try:
    WebDriverWait(driver,.1).until(EC.element_to_be_clickable((By.ID, "checkout_billing_address_province")))
except TimeoutException:
    print 'TIMEOUT STATE DROPDOWN'

Select(driver.find_element_by_id("checkout_billing_address_province")).select_by_visible_text(bill_state)

driver.find_element_by_id("checkout_billing_address_zip").send_keys(bill_zip)
driver.find_element_by_id("checkout_billing_address_phone").send_keys(bill_phone)

#Submit Order
#driver.find_element_by_name("button").click()

'''
for iframe in driver.find_elements_by_class_name("card-fields-iframe"):
    if 'name' in iframe.get_attribute("id"):
        print 'Name field found'
        driver.switch_to_frame(iframe)
        driver.find_element_by
        continue
    elif 'expiry' in iframe.get_attribute("id"):
        print 'Expiry field found'
        continue
    elif 'verification' in iframe.get_attribute("id"):
        print 'Verification value found'
        continue
    #print iframe.get_attribute("id")
    if 'number' in iframe.get_attribute("id"):
        print 'Number field found'
        driver.switch_to_frame(iframe)

        for digit in cc_num:
            result = attemptInput("number", digit, 5)
            print result
            driver.switch_to_default_content
        continue
'''

end = timer()
print "Runtime: " + str(end - start) + "s"
