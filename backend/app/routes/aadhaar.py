from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.schemas import AadhaarData
from app.utils.ocr import extract_text_from_image, parse_aadhaar_details

router = APIRouter()


@router.post(
    "/extract-aadhaar", response_model=AadhaarData, status_code=status.HTTP_200_OK
)
async def extract_aadhaar_details(file: UploadFile = File(...)):
    """
    Extracts Aadhaar card details (Name, DOB, Gender, Aadhaar Number) from an uploaded image.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File must be an image."
        )

    try:
        contents = await file.read()
        text = extract_text_from_image(contents)
        details = parse_aadhaar_details(text)

        return details
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}",
        )
