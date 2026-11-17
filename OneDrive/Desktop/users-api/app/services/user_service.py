from werkzeug.security import generate_password_hash

from app.dtos.user_dto import UserCreateDTO, UserPatchDTO
from app.errors import ConflictError, NotFoundError
from app.mappers.user_mapper import user_to_response_dto
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository | None = None):
        self.repository = repository or UserRepository()

    def create_user(self, dto: UserCreateDTO):
        if self.repository.get_by_email(dto.email):
            raise ConflictError("el email ya está registrado")
        if self.repository.get_by_username(dto.username):
            raise ConflictError("el username ya está en uso")
        user = User(
            username=dto.username,
            email=dto.email,
            password_hash=generate_password_hash(dto.password),
            full_name=dto.full_name,
        )
        self.repository.add(user)
        return user_to_response_dto(user)

    def list_users(self):
        return [user_to_response_dto(u) for u in self.repository.list()]

    def get_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("usuario no encontrado")
        return user_to_response_dto(user)

    def replace_user(self, user_id: int, dto: UserCreateDTO):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("usuario no encontrado")
        self._check_unique(dto.email, dto.username, exclude_id=user.id)
        user.username = dto.username
        user.email = dto.email
        user.password_hash = generate_password_hash(dto.password)
        user.full_name = dto.full_name
        self.repository.save(user)
        return user_to_response_dto(user)

    def patch_user(self, user_id: int, dto: UserPatchDTO):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("usuario no encontrado")
        new_email = dto.email if dto.email is not None else user.email
        new_username = dto.username if dto.username is not None else user.username
        self._check_unique(new_email, new_username, exclude_id=user.id)
        if dto.username is not None:
            user.username = dto.username
        if dto.email is not None:
            user.email = dto.email
        if dto.password is not None:
            user.password_hash = generate_password_hash(dto.password)
        if dto.full_name_provided:
            # full_name puede limpiarse explícitamente a null
            user.full_name = dto.full_name
        self.repository.save(user)
        return user_to_response_dto(user)

    def delete_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("usuario no encontrado")
        self.repository.delete(user)

    def _check_unique(self, email: str, username: str, exclude_id: int):
        existing_email = self.repository.get_by_email(email)
        if existing_email and existing_email.id != exclude_id:
            raise ConflictError("el email ya está registrado")
        existing_username = self.repository.get_by_username(username)
        if existing_username and existing_username.id != exclude_id:
            raise ConflictError("el username ya está en uso")
