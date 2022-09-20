# fastapi-fb-page-scraper
This is a simple fastapi app that aims to expose a scraping service that only supports `Facebook pages following a specific structure`.

### Installation
* set a virtual environment with pipenv,virtualenv..
* install the project dependencies using **requirements.txt** file
* start the service with this command : **uvicorn api.main:app --reload**

### Docs
* FastAPI provides automatic and interactive API documentation through Swagger UI
* The ID of each Page object is taken as the resource of it's facebook URL
  * if URL is `https://www.facebook.com/BBCnewsArabic`, the appropriate page ID is `BBCnewsArabic`
* A valid URL for this app is like `https://www.facebook.com/page/` or `https://facebook.com/page/` (No plain solution to translate the page from any language to english)

### Example pages to start try the api with
* [Foot 24 page](https://facebook.com/www.foot24.tn/)
* [Nessma sports page](https://www.facebook.com/sportnessma/)
* [BBC news page](https://www.facebook.com/BBCnewsArabic)
## Note
* You need to have **Chrome** and **MongoDB** Server installed in your machine in order to try out this prototype
* You don't need to provide your Facebook credentials or be logged into Facebook to try this app.
## TODO
* **Dockerize** the app with the **database** and allow opening the browser on the **client side**
