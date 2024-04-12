import logging
from contextlib import asynccontextmanager
from typing import Optional

import prisma
import prisma.enums
import project.create_user_account_service
import project.delete_user_account_service
import project.generate_image_service
import project.get_user_profile_service
import project.list_ai_models_service
import project.update_user_profile_service
import project.user_login_service
import project.user_logout_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="image maker",
    lifespan=lifespan,
    description="Based on the information gathered, your task involves creating images from input text utilizing advancements in AI technology. Specifically, you'll be leveraging the capabilities of sophisticated text-to-image AI models like DALL·E 2 by OpenAI, Google's Imagen, Midjourney, and Stable Diffusion by Stability AI. These models are distinguished by their ability to generate high-resolution images accurately reflecting the nuances of given textual descriptions. They offer improved fidelity, customization options, and accessibility compared to earlier models, enabling the creation of detailed and creative images based on specific themes, styles, or subjects of interest expressed in text. This project would involve integrating one or more of these AI technologies to develop a system that interprets textual inputs and produces corresponding images, capturing the specified details, themes, and styles as closely as possible.",
)


@app.post("/auth/login/", response_model=project.user_login_service.UserLoginResponse)
async def api_post_user_login(
    email: str, password: str
) -> project.user_login_service.UserLoginResponse | Response:
    """
    Authenticates a user and initiates a session.
    """
    try:
        res = await project.user_login_service.user_login(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/ai/models/", response_model=project.list_ai_models_service.ListModelResponse)
async def api_get_list_ai_models() -> project.list_ai_models_service.ListModelResponse | Response:
    """
    Provides a list of available AI models for image generation.
    """
    try:
        res = await project.list_ai_models_service.list_ai_models()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/account/",
    response_model=project.create_user_account_service.CreateUserResponse,
)
async def api_post_create_user_account(
    firstName: Optional[str], email: str, password: str, lastName: Optional[str]
) -> project.create_user_account_service.CreateUserResponse | Response:
    """
    Creates a new user account.
    """
    try:
        res = await project.create_user_account_service.create_user_account(
            firstName, email, password, lastName
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/user/account/{id}",
    response_model=project.delete_user_account_service.DeleteUserAccountResponse,
)
async def api_delete_delete_user_account(
    id: str,
) -> project.delete_user_account_service.DeleteUserAccountResponse | Response:
    """
    Deletes an existing user account.
    """
    try:
        res = await project.delete_user_account_service.delete_user_account(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/logout/", response_model=project.user_logout_service.LogoutResponse)
async def api_post_user_logout() -> project.user_logout_service.LogoutResponse | Response:
    """
    Terminates an authenticated session.
    """
    try:
        res = await project.user_logout_service.user_logout()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile/{id}/update",
    response_model=project.update_user_profile_service.UserProfileUpdateResponse,
)
async def api_put_update_user_profile(
    firstName: str, lastName: str, id: str, email: str, bio: Optional[str]
) -> project.update_user_profile_service.UserProfileUpdateResponse | Response:
    """
    Updates a user's profile information.
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            firstName, lastName, id, email, bio
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/profile/{id}",
    response_model=project.get_user_profile_service.UserProfileResponse,
)
async def api_get_get_user_profile(
    id: str,
) -> project.get_user_profile_service.UserProfileResponse | Response:
    """
    Retrieves a user's profile information.
    """
    try:
        res = await project.get_user_profile_service.get_user_profile(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/image/generate/",
    response_model=project.generate_image_service.GenerateImageResponse,
)
async def api_post_generate_image(
    text_description: str,
    ai_model: prisma.enums.AIModel,
    theme: Optional[str],
    style: Optional[str],
) -> project.generate_image_service.GenerateImageResponse | Response:
    """
    Generates an image based on user input using the selected AI model.
    """
    try:
        res = await project.generate_image_service.generate_image(
            text_description, ai_model, theme, style
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
