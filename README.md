# ShopifyImageRepo

### Project for the Winter 2022 - Shopify Developer Intern Challenge

The project contains an image repository with sample users and images. Users can login to access their photos and upload one or mulitple photos into their repository. 
User login passwords have been encrypted using SHA256 hashing before being stored in the database to provide secure password protection. 
When a user uploads images, the images will be validataed through their file type and file name before being saved. Users can also logout of their accounts returning them to the login page. 

The project was created using Python in the backend and Flask as the web framework. The database is created using sqlite3 and involves two tables,
one for storing images and one for storing users.

## Instructions

Ensure you have python3 and flask installed locally, and run `python app.py` to start the application. The webstie should be served at `http://127.0.0.1:5000/`.
