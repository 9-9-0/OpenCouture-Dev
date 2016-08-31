# Dev Notes
- 8/30: 
	- Look into the following libraries to use: mechanize, selenium (headless)
	- Clean up bodega.py once it's fully functional
	- !Figure out why item isn't showing up in cart despite importing the cookies (correctly?)
- 8/29: Review Unicode encodings, why writing to file has issues when it's not encoded correctly

# Current list of shops to implement:
-	[ ] Haven
-	[ ] Adidas
-	[ ] Bodega
-	[ ] END

# Design Considerations

Current Purchase Process:
- Navigate to desired product's webpage
- Request for webpage's HTML, begin a session
- Add shoe to cart
- Parse HTML for shoe size/colorway, save form data
- Send over the data ("Add To Cart" button triggers a POST method: http://shop.bdgastore.com/cart/add.js)
