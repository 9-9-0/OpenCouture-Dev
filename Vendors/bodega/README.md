# Notes

To run these scripts, make sure you add the required drivers (i.e. chromedriver, phantomJS) to the script's directory. Latest versions should work fine.

### bodegaSEL.py

Basic structure of the credit card input section on the checkout page is like this: 
```
<div><iframe><input></input></iframe><iframe>...</div>
```
div and each iframe are dynamic, so to avoid StaleElementReferenceExceptions you're going to have to manually examine when the div and iframes change based on what you type in the fields.
