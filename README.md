# ShopifyImageRepo

### Project for the Winter 2022 - Shopify Developer Intern Challenge

The project contains an image repository with sample users and images. Users can login to access their photos and upload one or mulitple photos into their repository. 
User login passwords have been encrypted using SHA256 hashing before being stored in the database to provide secure password protection. 
When a user uploads images, the images will be validataed through their file type and file name before being saved. Users can also logout of their accounts returning them to the login page. 

The project was created using Python in the backend and Flask as the web framework. The database is created using sqlite3 and involves two tables,
one for storing images and one for storing users.

## Instructions

Ensure you have python3 and flask installed locally, and run `python app.py` to start the application. The webstie should be served at `http://127.0.0.1:5000/`.

### **Login Credentials**
There are three users available for logging in.

| Username      | Password |
| ----------- | ----------- |
| bunny      | carrots       |
| cat   | salmon        |
| bird   | seeds        |


![image](https://user-images.githubusercontent.com/47133196/132923076-efddc30b-4559-45e4-a563-b85101f3a16b.png)

### **File Upload**

After logging in as one of the users, you will see their current images in their repository. You can select files to upload via the Choose Files button (only .png .jpg .gif files are allowed) then click Submit to upload the photos. The images will be shown immediately if you scroll down the page. Logging out can be done on the top left corner. The images will persist when you log out of a user and log back in.

![image](https://user-images.githubusercontent.com/47133196/132922904-8053a1a2-983e-4330-8dd8-1e5c8bb81b75.png)

## Future Goals

Ideally, I would have loved to add some automated tests to my application. I would have likely used pytest as the testing framework and would have created some tests for logging in and out and file uploads. In terms of features, I would have wanted to add account creation because currently the accounts are hardcoded. Other improvements I would want to do include storing the images themselves into database for more security, and adding the ability for users to delete photos that have been uploaded. 
