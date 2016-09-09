# Dev Notes
- 9/8 : 
	- Look into python's timeit functionality to time various operations
	- Revise the main README.md and remove MECH and SEL variants. Mechanize lacks functionality and Selenium may be too slow
	
	adidasREQ.py Specific:
	- At some point, make use of <option>'s data-maxavailable and data-status attributes for error checking in addToCart()
	- A consideration for the regex expression used: ^8+$ (matches shoe size 8). Pretty sure that this'll match 88, 808, 818, etc. Maybe look to refine this in case websites want to throw a curveball.
	- Issue occurs when matching the item.string content since the shoe size is embeddd in \n and \t. Two options: strip it with python's built in string function and then perform a regex search on it, or use a regex substitution. Temporarily going with the latter as someone mentioned it's actually quicker (COMPARE THE SPEEDS YOURSELF AT SOME POINT)
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
- Inject headers
- Request for webpage's HTML, begin a session
- Add shoe to cart
- Parse HTML for shoe size/colorway, save form data
- Send over the data ("Add To Cart" button triggers a POST method: http://shop.bdgastore.com/cart/add.js)
