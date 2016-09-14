# Dev Notes
- 9/13 :
	- More problems: Adidas has implemented a 10 minute checkout + Captcha on certain exclusive items (https://www.adidas.com/us/eqt-support-93-16-shoes/S79921.html)
	- Check DeathByCaptcha and see if their paid API is worth implementing
	- Code Issues: Shipping and Billing info gets posted, but subsequent retrieval of payment information page redirects to where delivery-start directs to. Find out what's going on
- 9/12 (Additional) :
	- Created a folder with all of the headers sent during various parts of the purchase process. The headers sent by the program should reflect these state changes.
	- Tentative, near-finalized post data for the ship/bill info written out. Saved the entire form that's sent within the HeadersForm folder
	- Don't use BeautifulSoup.findAll if .find can be used instead. Saves some overhead
- 9/12 :
	- Another potential checkout process. There's a mpstat.us post sent when you click "Review and Pay" on the shipping forms page. This may require us to look into Selenium or find a way to emulate an actual browser submitting this (with little overhead). Selenium Headless?
- 9/11 :
	- Potential problem found with Adidas' checkout process. There are two scripts in question: id="delivery-form-config" and the script that comes after it. I'm not sure if they package up the user's inputted data and then posts it up to the server, or if it's related to a process that occurs when the user gets the checkout page.
	- Anyhoooo, this is something to consider if the script doesn't work. Consulting an "expert" later for some advice. For now, the script will post the data with the names contained in the input fieldsets.
- 9/9 : 
	- Noticed that the headers of the get and post requests differed after inspecting them. Revised the headers and added functionality that modifies the referer key based on step in the process
	- Consider using Vultr and Blazing SEO to test mass executions next week
	- Add Error Handling Functionality once the checkout process for Adidas is complete
- 9/8 : 
- 	- **Design Modification**: Figure out if the current OOP model supports cookie persistence between adding to cart and checking out (for example: adding to the cart may succeed on the first attempt, but it may take multiple subsequent attempts to successfully checkout)
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
