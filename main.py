from fastapi import FastAPI,HTTPException,Response
from .database import get_all_posts, get_fb_page_by_id,create_fb_page,update_fb_page,delete_fb_page
from .schema import FacebookPage

app = FastAPI()


@app.get('/pages/all/')
async def get_all():
    response = await get_all_posts()
    return response

@app.get('/pages/{id}',response_model=FacebookPage)
async def get_by_id(id:str):
    response = await get_fb_page_by_id(id)
    if response:
        return response
    raise HTTPException(404,f"no page item with this key : {id}")

@app.post('/pages/',response_model=FacebookPage)
async def create_page(page:FacebookPage):
    response = await create_fb_page(page.dict())
    if response:
        return response
    raise(HTTPException(400,"bad request, something went wrong"))

@app.put('/pages/{id}',response_model=FacebookPage)
async def update_page(id:str,page:FacebookPage):
    response = await update_fb_page(id,page.dict())
    if response:
        return response
    raise HTTPException(400,f"bad request, something went wrong")

# TODO change url to id (can't include url into another)
@app.delete('/pages/{id}')
async def delete_page(id:str):
    response = await delete_fb_page(id)
    if response:
        return Response(f"page with id : {id} successfully deleted")
    raise HTTPException(404,f"no page item with this key : {id}") 

