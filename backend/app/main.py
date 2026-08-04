from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
import models
import schemas

from auth import get_current_user
from hashing import hash_password, verify_password
from security import create_access_token, create_refresh_token

from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


Base.metadata.create_all(bind=engine)


app = FastAPI()



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@app.get("/")
def home():

    return {
        "message": "API is working"
    }



# ================= REGISTER =================


@app.post(
    "/register",
    response_model=schemas.UserResponse
)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_email = db.query(models.User).filter(
        models.User.email == user.email
    ).first()


    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )



    existing_username = db.query(models.User).filter(
        models.User.username == user.username
    ).first()


    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )



    new_user = models.User(

        username=user.username,

        email=user.email,

        password=hash_password(user.password)

    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)



    return {

        "id": new_user.id,

        "username": new_user.username,

        "email": new_user.email

    }




# ================= LOGIN =================


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    print("USERNAME:", form_data.username)
    print("PASSWORD:", form_data.password)

    db_user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    print("USER FROM DB:", db_user)

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    password_check = verify_password(
        form_data.password,
        db_user.password
    )

    print("PASSWORD CHECK:", password_check)


    if not password_check:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )


    print("PASSWORD OK")


    access_token = create_access_token({
        "sub": str(db_user.id)
    })


    refresh_token = create_refresh_token({
        "sub": str(db_user.id)
    })


    print("TOKENS CREATED")


    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }




# ================= REFRESH TOKEN =================


@app.post("/refresh")
def refresh_token(

    data: schemas.RefreshTokenRequest

):

    try:


        payload = jwt.decode(

            data.refresh_token,

            SECRET_KEY,

            algorithms=[ALGORITHM]

        )



        if payload.get("type") != "refresh":

            raise HTTPException(

                status_code=401,

                detail="Invalid refresh token"

            )



        user_id = payload.get("sub")



        if user_id is None:

            raise HTTPException(

                status_code=401,

                detail="Invalid refresh token"

            )



        new_access_token = create_access_token({

            "sub": user_id

        })



        return {

            "access_token": new_access_token,

            "token_type": "bearer"

        }



    except ExpiredSignatureError:


        raise HTTPException(

            status_code=401,

            detail="Refresh token expired"

        )



    except JWTError:


        raise HTTPException(

            status_code=401,

            detail="Invalid refresh token"

        )





# ================= PROFILE =================


@app.get(

    "/users/me",

    response_model=schemas.UserResponse

)

def get_profile(

    user_id: int = Depends(get_current_user),

    db: Session = Depends(get_db)

):


    user = db.query(models.User).filter(

        models.User.id == user_id

    ).first()



    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )



    return {

        "id": user.id,

        "username": user.username,

        "email": user.email

    }


print("ALL ROUTES:")

for route in app.routes:

    print(route.path, route.methods)