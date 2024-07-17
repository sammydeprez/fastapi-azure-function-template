import fastapi

router = fastapi.APIRouter()

@router.post("/hello_world")
async def chat() -> str:
    return "Hello World via POST"


@router.get("/hello_world")
async def chat() -> str:
    return "Hello World via GET"