from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId

from auth.jwt_handler import oauth2_scheme, get_password_hash, verify_token, verify_password, create_access_token
from models.user import UserOut, UserCreate, UserInDB
from utils import get_user, get_all_users, insert_user

router = APIRouter()


@router.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    user = get_user({"_id": ObjectId(user_id)})
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    if user.role not in ["admin", "films", "people", "locations", "species", "vehicles"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    existing_user = get_user({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(user.password)
    new_user = UserInDB(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role=user.role
    )
    result = insert_user(new_user.dict())

    return UserOut(id=str(result.inserted_id), **new_user.dict())


@router.get("/users", response_model=list[UserOut])
async def get_users(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    user = get_user({"_id": ObjectId(user_id)})
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    users = get_all_users()

    return [UserOut(**{**x, 'id': str(x['_id'])}) for x in users]


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user["_id"]), "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}
