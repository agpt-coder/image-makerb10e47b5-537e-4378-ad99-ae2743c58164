from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserProfileUpdateResponse(BaseModel):
    """
    The response model for the update user profile endpoint. It contains the updated information of the user profile to confirm the changes applied.
    """

    id: str
    email: str
    firstName: str
    lastName: str
    bio: Optional[str] = None
    updatedAt: datetime


async def update_user_profile(
    id: str, email: str, firstName: str, lastName: str, bio: Optional[str]
) -> UserProfileUpdateResponse:
    """
    Updates a user's profile information.

    Args:
    id (str): The identifier of the user whose profile is to be updated. This should match the user's ID in the database and the authentication token's subject.
    email (str): The new email address for the user. Must be unique across the system.
    firstName (str): The user's new first name.
    lastName (str): The user's new last name.
    bio (Optional[str]): A brief description about the user or biography. This field is optional.

    Returns:
    UserProfileUpdateResponse: The response model for the update user profile endpoint. It contains the updated information of the user profile to confirm the changes applied.
    """
    await prisma.models.User.prisma().update(where={"id": id}, data={"email": email})
    updated_profile = await prisma.models.Profile.prisma().update(
        where={"userId": id},
        data={
            "firstName": firstName,
            "lastName": lastName,
            "updatedAt": datetime.now(),
        },
    )
    return UserProfileUpdateResponse(
        id=id,
        email=email,
        firstName=firstName,
        lastName=lastName,
        bio=bio,
        updatedAt=updated_profile.updatedAt,
    )
