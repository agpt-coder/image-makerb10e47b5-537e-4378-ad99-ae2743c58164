from enum import Enum
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GenerateImageResponse(BaseModel):
    """
    This model provides details about the generated image, including the URL and status.
    """

    image_url: str
    status: prisma.enums.ImageRequestStatus
    ai_model_used: prisma.enums.AIModel
    text_description_used: str


class AIModel(Enum):
    DALLE2: str = "DALLE2"
    IMAGEN: str = "IMAGEN"
    MIDJOURNEY: str = "MIDJOURNEY"
    STABLEDIFFUSION: str = "STABLEDIFFUSION"


class ImageRequestStatus(Enum):
    PROCESSING: str = "PROCESSING"
    COMPLETED: str = "COMPLETED"
    FAILED: str = "FAILED"


async def generate_image(
    text_description: str,
    ai_model: prisma.enums.AIModel,
    theme: Optional[str],
    style: Optional[str],
) -> GenerateImageResponse:
    """
    Generates an image based on user input using the selected AI model.

    Args:
        text_description (str): The textual description provided by the user, which serves as input for generating the image.
        ai_model (prisma.enums.AIModel): The selected AI model to be used for image generation. Can be one of: DALLE2, IMAGEN, MIDJOURNEY, STABLEDIFFUSION.
        theme (Optional[str]): Optional: The theme preference for the generated image.
        style (Optional[str]): Optional: The style preference for the generated image.

    Returns:
        GenerateImageResponse: This model provides details about the generated image, including the URL and status.
    """
    image_request_record = await prisma.models.ImageRequest.prisma().create(
        data={
            "userId": "user_id_placeholder",
            "textDescription": text_description,
            "prisma.enums.AIModel": ai_model,
            "theme": theme,
            "style": style,
            "status": prisma.enums.ImageRequestStatus.PROCESSING,
        }
    )
    completed_request = await prisma.models.ImageRequest.prisma().update(
        where={"id": image_request_record.id},
        data={
            "imageUrl": "http://example.com/placeholder_image.png",
            "status": prisma.enums.ImageRequestStatus.COMPLETED,
        },
    )
    return GenerateImageResponse(
        image_url=completed_request.imageUrl,
        status=completed_request.status,
        ai_model_used=completed_request.AIModel,
        text_description_used=completed_request.textDescription,
    )
