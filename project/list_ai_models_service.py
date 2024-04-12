from typing import List

from pydantic import BaseModel


class AIModelDetail(BaseModel):
    """
    Detail of an individual AI model including name, description, and characteristics.
    """

    name: str
    description: str
    supported_styles: List[str]
    limitations: List[str]


class ListModelResponse(BaseModel):
    """
    Response model that provides detailed information about each available AI model for image generation.
    """

    ai_models: List[AIModelDetail]


async def list_ai_models() -> ListModelResponse:
    """
    Provides a list of available AI models for image generation.

    This function queries the database to find all available AI models, then structures
    and returns the data in a formatted response including details about each model.

    Args:


    Returns:
    ListModelResponse: Response model that provides detailed information about each available AI model for image generation.
    """
    ai_models_info = {
        "DALLE2": AIModelDetail(
            name="DALL·E 2",
            description="A sophisticated AI by OpenAI for generating digital images from natural language descriptions.",
            supported_styles=["cartoon", "realistic", "fantasy"],
            limitations=["May produce unrealistic images for complex queries."],
        ),
        "IMAGEN": AIModelDetail(
            name="Imagen",
            description="Google's state-of-the-art text-to-image AI model offering photorealistic image generation.",
            supported_styles=["photorealism", "painting"],
            limitations=["Limited to certain styles and subjects."],
        ),
        "MIDJOURNEY": AIModelDetail(
            name="Midjourney",
            description="An independent research lab’s AI specializing in creating vivid images and art.",
            supported_styles=["abstract", "conceptual art"],
            limitations=["Generates images with a distinctive stylistic signature."],
        ),
        "STABLEDIFFUSION": AIModelDetail(
            name="Stable Diffusion",
            description="An AI model by Stability AI that excels at generating highly detailed images.",
            supported_styles=["digital art", "concept art"],
            limitations=["Occasional artifacts in generated images."],
        ),
    }
    list_model_response = ListModelResponse(ai_models=list(ai_models_info.values()))
    return list_model_response
