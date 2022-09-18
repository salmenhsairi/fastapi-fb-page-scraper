from typing_extensions import Required
from pydantic import BaseModel,Field
from typing import List,Union

class FacebookPost(BaseModel):
    description:Union[str,None]
    reacts:Union[str,None]
    comments:Union[str,None]
    shares:Union[str,None]

class FacebookPage(BaseModel):
    url:str
    key:str 
    title:Union[str,None]
    location:Union[str,None]
    website:Union[str,None]
    email:Union[str,None]
    created_at:Union[str,None]
    like:Union[str,None]
    follow:Union[str,None]
    checked_in:Union[str,None]
    posts:Union[List[FacebookPost],None] = None

