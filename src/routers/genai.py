from fastapi import Body, APIRouter, status, Response, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from resources.ocigenai import OciGenai
from resources.basic_auth import Auth

import json

router = APIRouter(
    prefix="/20231130/actions",
    tags=["ocigenai"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/{endpoint}",
    summary="Execute workflow (sync)",
    dependencies=[Depends(Auth.verify_auth)],
)
async def process_dynamic_endpoint(
    endpoint: str,
    data: dict = Body(...),
    request: Request = None,
    response: Response = None,
):
    controller = OciGenai()
    response = controller.split_routes(data=data,endpoint=endpoint)
    try:
        if response.status == 200:
            response.status_code = status.HTTP_200_OK
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
    except Exception as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    print(response.data.model_id)
    return response