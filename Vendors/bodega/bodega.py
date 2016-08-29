import requests
from bs4 import BeautifulSoup
import code
import re

# Early Link #
bool_direct_link = False

# URL Presets #
# Move these members to a profile class eventually #
URL_vendor_url  = 'http://shop.bdgastore.com/'
URL_direct_link = 'http://shop.bdgastore.com/collections/footwear/products/y-3-pureboost-zg'

#################
## Main Script ##
#################

user_session = requests.Session()
session_get  = user_session.get(URL_direct_link)

print 'Status of requests.get: ' + str(session_get.status_code)

#print ping_vendor.text
#bodegaProdFile = open('test.html', 'wb')
#for chunk in ping_vendor.iter_content(100000):
#    bodegaProdFile.write(chunk)

###############################
#See README for how to proceed#
###############################

#print session_get.content

prod_soup = BeautifulSoup(session_get.content, "lxml")
#Check that the lxml parser works for html
#Use SoupStrainer to improve parsing efficiency

user_size = 8

### Block used to save HTML tree of interest ###
################################################
# Check Dev Notes for a Concept Review #
ResultSet = prod_soup.find_all('form', {'id' : 'qv-form'})
with open('input', 'wb') as ResultSetFile:
    ResultSetFile.write(str(ResultSet))
ResultSetString = unicode.join(u'\n',map(unicode,ResultSet))
print ResultSetString

ResultSoup = BeautifulSoup(ResultSetString, "lxml")
print ResultSoup.prettify()
with open('bodegaForm.html', 'wb') as bodegaFormFile:
    bodegaFormFile.write(ResultSoup.prettify())
################################################


#for size in prod_soup.findAll('option'):
#    if size.parent.name == 'select':
#        print size
#        print size['value']

#print '\n'

#arr = prod_soup.findAll('option')
#print arr[0]
#print arr[1]
#print type(arr[0])

#post_data = {
#http://shop.bdgastore.com/cart/add.js

#Uncomment ln 3 and 43 to launch into interpreter
#code.interact(local=locals())

