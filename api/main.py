from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from .database import get_all_pages, get_fb_page_by_id, create_fb_page, update_fb_page, delete_fb_page
from .scraper import scrap_fb_page, check_valid_url
from .schema import FacebookPage, FacebookURL
app = FastAPI()


@app.route("/")
async def docs_redirect(request):
    return RedirectResponse(url='/docs')


@app.get('/pages/all/')
async def get_all():
    response = await get_all_pages()
    return response


@app.get('/pages/{id}', response_model=FacebookPage)
async def get_by_id(id: str):
    response = await get_fb_page_by_id(id)
    if response:
        return response
    raise HTTPException(404, f"no page item with this key : {id}")


@app.post('/pages/scrap', response_model=FacebookPage)
async def create_page_from_url(url: FacebookURL):
    if not url.url or not check_valid_url(url.url):
        raise (
            HTTPException(400, 'please make sure that the provided URL is a valid facebook URL like https://www.facebook.com/example'))
    try:
        fb_page_data = await scrap_fb_page(url.url)
        fb_page_exists = await get_fb_page_by_id(fb_page_data['key'])
        if fb_page_exists:
            update_response = await update_fb_page(fb_page_data['key'], fb_page_data)
            if update_response:
                return update_response
            else:
                raise (Exception('unable to update the page, something went wrong'))
        else:
            create_response = await create_fb_page(fb_page_data)
            if create_response:
                return create_response
            else:
                raise (Exception('unable to create the page, something went wrong'))
    except Exception as e:
        # raise HTTPException(400, "bad request, something went wrong")
        # raise
        raise HTTPException(400, str(e))


@app.post('/pages/create', response_model=FacebookPage)
async def create_page(page: FacebookPage):
    response = await create_fb_page(page.dict())
    if response:
        return response
    raise (HTTPException(400, "bad request, something went wrong"))


@app.put('/pages/{id}', response_model=FacebookPage)
async def update_page(id: str, page: FacebookPage):
    response = await update_fb_page(id, page.dict())
    if response:
        return response
    raise HTTPException(400, f"bad request, something went wrong")

# TODO change url to id (can't include url into another)


@app.delete('/pages/delete/{id}')
async def delete_page(id: str):
    response = await delete_fb_page(id)
    if response:
        return Response(f"page with id : {id} successfully deleted")
    raise HTTPException(404, f"no page item with this key : {id}")
