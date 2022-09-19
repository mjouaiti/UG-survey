# import email
# from email import message
# import time
from pickletools import long1
from fastapi import Body, FastAPI, Response, status, HTTPException

from app.db import database, User
from app.schemas import *
from data_dcarte.get_dcarte_data import *
from app.schemas import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from nlp.summarisation import *


# Initialize the FastAPI app for a simple web server
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# get all users
@app.get("/users")
async def get_users():
    users = await User.objects.all()
    # return 
    return jsonable_encoder(users)


# get single user data
@app.get("/user/{id}")
async def get_user(id):
    user = await User.objects.get_or_none(id=id)
    if not user:
        user = await User.objects.get_or_none(email=id)
        if not user:
            user = await User.objects.get_or_none(name=id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail=f"user with id {id} not found.")
    print(type(user))
    return jsonable_encoder(user)

# update single user data
@app.put("/user/{id}")
async def update_user(id:int, user:UserBase):
    # await user.save_related(follow=True, save_all=True)
    u = await User.objects.get(pk=id)
    if not user.id:
        user.id = u.id
    await u.update(**user.dict())
    return u

#delete single user data
@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, user: UserBase = None):
    if user:
        return {"deleted_rows": await user.delete()}
    user_db = await User.objects.get(pk=id)
    await user_db.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# add a single user
@app.post('/user', status_code=status.HTTP_201_CREATED)
async def new_user(user:UserBase):
    await User.objects.get_or_create(user)
    return jsonable_encoder(user)



# checking single user data
####### to be continued
@app.get("/user_history/{id}")
async def get_user_history(id: int):
    user = await User.objects.get_or_none(id=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id {id} not found.")
    return jsonable_encoder({"user_history":"history"})

# add a single user
@app.post('/add_user', status_code=status.HTTP_201_CREATED)
async def new_user(user:UserBase):
    await user.save()
    return jsonable_encoder(user)



# @app.post("/summdoc")
# def summarise_post(text:Text_Input):
#     # print(text)
#     summary = top_sentence(text.text, 500)
#     return{"input":text,
#             "summarisation": summary}

@app.post("/conv_user", status_code=status.HTTP_201_CREATED)
async def conv_by_user(response:UserResponse):
    # print(text)
    await response.save()
    return jsonable_encoder(response)

@app.post("/conv_system", status_code=status.HTTP_201_CREATED)
async def conv_by_user(response:SystemResponse):
    # print(text)
    await response.save()
    return jsonable_encoder(response)




@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    await User.objects.get_or_create(name='testuser', email="test@test.com",major='mechanical engineering')


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()



