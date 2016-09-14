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
