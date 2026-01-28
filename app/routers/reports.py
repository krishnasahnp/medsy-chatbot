from fastapi import APIRouter

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def generate_report():
    return {"report_id": 123, "content": "Patient health summary placeholder."}
