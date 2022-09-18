from .schema import FacebookPage,FacebookPost
from motor import motor_asyncio

client = motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

database = client.FB_WEBSCRAPING
collection = database.FB_Page

async def get_fb_page_by_id(id:str):
    fb_page = await collection.find_one({"key":id})
    return fb_page
    
async def get_all_posts():
    fb_pages = []
    cursor = collection.find({})
    async for fb_page in cursor:
        fb_pages.append(FacebookPage(**fb_page))
    return fb_pages

async def create_fb_page(fb_page):
    response = await get_fb_page_by_id(fb_page['key'])
    if not response:
        fb_page = {k:v for k,v in fb_page.items() if v}
        # fb_page_posts = fb_page['posts']
        if 'posts' in fb_page and fb_page['posts']:
            fb_page['posts'] = [{k:v for k,v in fb_post.items() if v} for fb_post in fb_page['posts']]
        result = await collection.insert_one(fb_page)
        if result:
            return fb_page

async def update_fb_page(id:str,fb_page):
    new_key = fb_page['key']
    if new_key != id and await get_fb_page_by_id(new_key):
        return False
    delete_status = await  delete_fb_page(id)
    if delete_status:
        response = await create_fb_page(fb_page)
        if response:
            return fb_page

async def delete_fb_page(id):
    response = await get_fb_page_by_id(id)
    if response:
        await collection.delete_one({"key":id})
        return True
    return False
