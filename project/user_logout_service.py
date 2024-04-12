from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class LogoutResponse(BaseModel):
    """
    Indicates the result of the logout request, primarily signaling whether the session was terminated successfully.
    """

    success: bool
    message: Optional[str] = None


async def user_logout() -> LogoutResponse:
    """
    Terminates an authenticated session by performing necessary clean-up in the database
    and potentially invalidating any authentication tokens. This function simulates a
    logout process by marking the latest access log entry with a note indicating logout,
    assuming in a fully implemented scenario there would be a more direct mechanism
    for invalidating a user's active session or authentication token.

    Args:
        None

    Returns:
    LogoutResponse: Indicates the result of the logout request, primarily signaling whether
                     the session was terminated successfully.
    """
    try:
        user_id = "example-user-id"
        last_access_log = await prisma.models.AccessLog.prisma().find_many(
            where={"userId": user_id}, order={"accessedAt": "desc"}, take=1
        )
        if last_access_log:
            access_log_entry = last_access_log[0]
            await prisma.models.AccessLog.prisma().update(
                where={"id": access_log_entry.id},
                data={"endpoint": f"{access_log_entry.endpoint} - User logged out."},
            )
        return LogoutResponse(success=True, message="User logged out successfully.")
    except Exception as e:
        return LogoutResponse(success=False, message=f"Failed to log out: {str(e)}")
