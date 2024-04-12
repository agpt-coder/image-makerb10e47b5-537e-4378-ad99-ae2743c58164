from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """
    The response object containing user profile information. This is based on both the User and Profile models but potentially includes sanitized or selected data for privacy considerations.
    """

    user_id: str
    email: str
    firstName: str
    lastName: str
    role: prisma.enums.UserRole
    createdAt: datetime
    updatedAt: datetime


async def get_user_profile(id: str) -> UserProfileResponse:
    """
    Retrieves a user's profile information based on the given user id.

    Args:
        id (str): The unique identifier of the user. This corresponds to the userId in the User and Profile database models.

    Returns:
        UserProfileResponse: The response object containing user profile information. This is based on both the User and Profile models but potentially includes sanitized or selected data for privacy considerations.

    Example:
        id = 'some-uuid-here'
        profile = await get_user_profile(id)
        print(profile)
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": id}, include={"profiles": True}
    )
    if not user:
        raise ValueError("User not found")
    profile_data = user.profiles[0] if user.profiles else None
    response = UserProfileResponse(
        user_id=user.id,
        email=user.email,
        firstName=profile_data.firstName if profile_data else None,
        lastName=profile_data.lastName if profile_data else None,
        role=user.role,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt,
    )
    return response
