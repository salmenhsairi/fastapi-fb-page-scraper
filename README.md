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

### Example pages to start try the api with
* [Foot 24 page](https://facebook.com/www.foot24.tn/)
* [Nessma sports page](https://www.facebook.com/sportnessma/)
* [BBC news page](https://www.facebook.com/BBCnewsArabic)
## Note
* You need to have **Chrome** and **MongoDB** Server installed in your machine in order to try out this prototype
## TODO
* **Dockerize** the app with the **database** and allow opening the browser on the **client side**
