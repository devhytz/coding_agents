import re
from dataclasses import dataclass
from typing import Optional

from app.errors import ValidationError

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_email(email):
    if not email or not EMAIL_RE.match(email):
        raise ValidationError("email inválido")


def _validate_username(username):
    if not username or len(username.strip()) < 3:
        raise ValidationError("username es requerido y debe tener al menos 3 caracteres")


def _validate_password(password):
    if not password or len(password) < 6:
        raise ValidationError("password es requerido y debe tener al menos 6 caracteres")


@dataclass
class UserCreateDTO:
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValidationError("el cuerpo de la solicitud debe ser un objeto JSON")
        username = (data.get("username") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        full_name = data.get("full_name")
        _validate_username(username)
        _validate_email(email)
        _validate_password(password)
        if full_name is not None:
            full_name = str(full_name).strip()
        return cls(username=username, email=email, password=password, full_name=full_name)


@dataclass
class UserPatchDTO:
    """Actualización parcial (PATCH): solo los campos presentes."""

    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    full_name_provided: bool = False

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValidationError("el cuerpo de la solicitud debe ser un objeto JSON")
        dto = cls()
        if "username" in data:
            username = (data.get("username") or "").strip()
            _validate_username(username)
            dto.username = username
        if "email" in data:
            email = (data.get("email") or "").strip().lower()
            _validate_email(email)
            dto.email = email
        if "password" in data:
            password = data.get("password") or ""
            _validate_password(password)
            dto.password = password
        if "full_name" in data:
            full_name = data.get("full_name")
            dto.full_name = str(full_name).strip() if full_name is not None else None
            dto.full_name_provided = True
        if dto.username is None and dto.email is None and dto.password is None and not dto.full_name_provided:
            raise ValidationError("no se enviaron campos para actualizar")
        return dto


@dataclass
class UserResponseDTO:
    id: int
    username: str
    email: str
    full_name: Optional[str]
    created_at: str
    updated_at: str

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
