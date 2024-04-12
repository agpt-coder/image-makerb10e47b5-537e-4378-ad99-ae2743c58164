import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserAccountResponse(BaseModel):
    """
    Provides feedback on the successful deletion of a user account. This confirmation is necessary for the client to understand the result of their deletion request.
    """

    message: str


async def delete_user_account(id: str) -> DeleteUserAccountResponse:
    """
    Deletes an existing user account from the database based on the given unique identifier (ID).

    If the user account exists and is successfully deleted, a confirmation message is returned.
    Otherwise, if the user account cannot be found or cannot be deleted, a failure message is returned.

    Args:
    - id (str): The unique identifier of the user account to be deleted.

    Returns:
    - DeleteUserAccountResponse: An instance of DeleteUserAccountResponse containing a message indicating
                                 whether the deletion was successful or not.

    Example:
    - delete_user_account("some-unique-user-id") -> DeleteUserAccountResponse(message="User account with ID some-unique-user-id has been successfully deleted.")
    - delete_user_account("non-existent-user-id") -> DeleteUserAccountResponse(message="Failed to delete user account with ID non-existent-user-id.")
    """
    try:
        deleted_user = await prisma.models.User.prisma().delete(where={"id": id})
        return DeleteUserAccountResponse(
            message=f"User account with ID {id} has been successfully deleted."
        )
    except Exception as e:
        return DeleteUserAccountResponse(
            message=f"Failed to delete user account with ID {id}."
        )
