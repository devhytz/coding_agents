class ValidationError(Exception):
    """Los datos de entrada no cumplen el contrato esperado."""


class NotFoundError(Exception):
    """El recurso solicitado no existe."""


class ConflictError(Exception):
    """La operación entra en conflicto con el estado actual (p. ej. email duplicado)."""
