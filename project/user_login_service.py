import bcrypt
import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserInfo(BaseModel):
    """
    This complex type contains identifying information about the user.
    """

    name: str
    email: str
    role: prisma.enums.UserRole


class UserLoginResponse(BaseModel):
    """
    The response sent back to the user upon a successful login. Includes a session token and potentially user profile information.
    """

    session_token: str
    user_info: UserInfo


async def user_login(email: str, password: str) -> UserLoginResponse:
    """
    Authenticates a user and initiates a session.

    Args:
        email (str): The registered email address of the user trying to login.
        password (str): The password corresponding to the user's account. This should be securely transmitted and handled.

    Returns:
        UserLoginResponse: The response sent back to the user upon a successful login. Includes a session token and potentially user profile information.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user:
        raise ValueError("User not found")
    password_match = bcrypt.checkpw(
        password.encode("utf-8"), user.password.encode("utf-8")
    )
    if not password_match:
        raise ValueError("Invalid password")
    session_token = "generated_session_token"
    user_info = prisma.models.User.parse_obj(user)
    return UserLoginResponse(session_token=session_token, user_info=user_info)
