from app.dtos.user_dto import UserResponseDTO
from app.models.user import User


def user_to_response_dto(user: User) -> UserResponseDTO:
    return UserResponseDTO(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        created_at=user.created_at.isoformat() if user.created_at else None,
        updated_at=user.updated_at.isoformat() if user.updated_at else None,
    )
