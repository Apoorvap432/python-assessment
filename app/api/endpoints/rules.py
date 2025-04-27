from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_rules():
    return {"message": "Transformation rules endpoint is working!"}
