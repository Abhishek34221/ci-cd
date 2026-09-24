from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from models.destination import Destination


router = APIRouter(
    prefix="/destinations",
    tags=["Destinations"]
)


# =========================================================
# PYDANTIC MODEL
# =========================================================

class DestinationCreate(BaseModel):
    name: str
    country: str
    rating: float
    price: str
    description: str
    image: str
    status: str = "active"
    code: Optional[str] = None


# =========================================================
# CREATE DESTINATION
# POST /destinations/
# =========================================================

@router.post("/")
async def create_destination(destination: DestinationCreate):

    try:

        new_destination = Destination(
            name=destination.name,
            country=destination.country,
            rating=destination.rating,
            price=destination.price,
            description=destination.description,
            image=destination.image,
            status=destination.status,
            code=destination.code,
            favorite=False
        )

        new_destination.save()

        return {
            "message": "Destination created successfully",
            "id": str(new_destination.id)
        }

    except Exception as e:

        print("CREATE DESTINATION ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GET DESTINATIONS
# GET /destinations/
# =========================================================

@router.get("/")
async def get_destinations():

    try:

        destinations = Destination.objects()

        result = []

        for destination in destinations:

            result.append({
                "id": str(destination.id),
                "name": destination.name,
                "country": destination.country,
                "rating": destination.rating,
                "price": destination.price,
                "description": destination.description,
                "image": destination.image,
                "status": destination.status,
                "code": destination.code,
                "favorite": destination.favorite
            })

        return result

    except Exception as e:

        print("GET DESTINATIONS ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# DELETE DESTINATION
# DELETE /destinations/{id}
# =========================================================

@router.delete("/{destination_id}")
async def delete_destination(destination_id: str):

    try:

        destination = Destination.objects(
            id=destination_id
        ).first()

        if not destination:

            raise HTTPException(
                status_code=404,
                detail="Destination not found"
            )

        destination.delete()

        return {
            "message": "Destination deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:

        print("DELETE ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )