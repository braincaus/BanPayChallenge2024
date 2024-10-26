from fastapi import APIRouter, Depends, HTTPException
import httpx
from bson import ObjectId

from auth.jwt_handler import verify_token, oauth2_scheme
from utils import get_user

router = APIRouter()


BASE_URL = "https://ghibliapi.vercel.app"

ROLE_PERMISSIONS = {
    "films": "films",
    "people": "people",
    "locations": "locations",
    "species": "species",
    "vehicles": "vehicles"
}


@router.get("/ghibli/{category}")
async def get_ghibli_data(category: str, token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    user = get_user({"_id": ObjectId(user_id)})

    if category not in ROLE_PERMISSIONS:
        raise HTTPException(status_code=400, detail="Invalid category")

    if user['role'] != ROLE_PERMISSIONS[category] and user['role'] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized for this category")

    url = f"https://ghibliapi.vercel.app/{category}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Studio Ghibli API")

    return response.json()
