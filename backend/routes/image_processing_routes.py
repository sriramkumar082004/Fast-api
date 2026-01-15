import os
import io
import requests
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter()

APY_URL = "https://api.apyhub.com/processor/image/change-background/file"


@router.post("/change-background")
async def change_background(
    image: UploadFile = File(...),
    background_image: UploadFile = File(None),
    background_color: str = Form(None),
):
    # Load token from environment
    apy_token = os.getenv("APY_TOKEN")
    if not apy_token:
        raise HTTPException(status_code=500, detail="APY_TOKEN is not configured.")

    # Default to white background if neither image nor color is provided
    if not background_image and not background_color:
        background_color = "#ffffff"

    headers = {"apy-token": apy_token}

    files = {"image": (image.filename, image.file, image.content_type)}

    if background_image:
        files["background_image"] = (
            background_image.filename,
            background_image.file,
            background_image.content_type,
        )

    data = {}
    if background_color:
        data["background_color"] = background_color

    try:
        response = requests.post(APY_URL, headers=headers, files=files, data=data)
        response.raise_for_status()

        # Determine content type from response headers or default to png/jpeg matches
        content_type = response.headers.get("Content-Type", "image/png")

        return StreamingResponse(io.BytesIO(response.content), media_type=content_type)

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Image processing failed: {str(e)}"
        )
