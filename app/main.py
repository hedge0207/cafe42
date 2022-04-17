import uvicorn
from datetime import timedelta

from fastapi import APIRouter, FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from model import Token, AdminPost, fake_users_db
from auth import authenticate_user, create_access_token, get_current_user
from config import config
from repository import create_admin_post, get_admin_post, update_admin_post, delete_admin_post


app = FastAPI()
router = APIRouter()

@app.on_event('startup')
def startup():
    from mongo import connect_mongo
    connect_mongo()

@app.on_event('shutdown')
def shutdown():
    from mongo import disconect_mongo
    disconect_mongo()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.token_expire_minutes)
    # JWT access token을 생성하고 반환한다.
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/admin/post")
async def create_post(post:AdminPost, user = Depends(get_current_user)):
    create_admin_post(post)

@router.get("/admin/post/{post_id}")
async def get_post(post_id: str, post:AdminPost):
    return get_admin_post(post_id)

@router.put("/admin/post/{post_id}")
async def get_post(post_id: str, post:AdminPost):
    update_admin_post(post_id, post)

@router.delete("/admin/post/{post_id}")
async def get_post(post_id: str):
    delete_admin_post(post_id)


app.include_router(router, prefix="/cafe42/v1")

if __name__=="__main__":
    uvicorn.run("main:app", port=8080, reload=True)
