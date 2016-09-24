from selenium import webdriver
from timeit import default_timer as timer

start = timer()

driver = webdriver.Firefox()
driver.get("http://www.adidas.com/us/shoes")

end = timer()

print 'Runtime: ' + str(end - start)

