from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    Model for the response returned by the system upon successful creation of a user account. It should confirm the account has been created.
    """

    userId: str
    email: str
    message: str


async def create_user_account(
    email: str, password: str, firstName: Optional[str], lastName: Optional[str]
) -> CreateUserResponse:
    """
    Creates a new user account.

    This function creates a new user account with the provided email and password, and optionally, first and last name.
    The password is securely hashed before storage. It verifies if the email is unique within the system.

    Args:
    email (str): Email address for the new user account. It must be unique across the system.
    password (str): Secure password for the new user account. This should be stored securely and never returned in API responses.
    firstName (Optional[str]): Optional first name of the user for personalization.
    lastName (Optional[str]): Optional last name of the user for personalization.

    Returns:
    CreateUserResponse: Model for the response returned by the system upon successful creation of a user account. It should confirm the account has been created.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        raise ValueError(
            "The provided email address is already associated with an existing account."
        )
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    user = await prisma.models.User.prisma().create(
        data={
            "email": email,
            "password": hashed_password,
            "profiles": {"create": {"firstName": firstName, "lastName": lastName}},
        }
    )
    return CreateUserResponse(
        userId=user.id,
        email=user.email,
        message="prisma.models.User account created successfully.",
    )
