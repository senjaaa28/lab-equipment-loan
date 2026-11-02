class ValidationError(ValueError):
    def __init__(self, message="Input tidak valid."):
        super().__init__(message)


class NotFoundError(LookupError):
    def __init__(self, message="Data tidak ditemukan."):
        super().__init__(message)


def require_non_empty_string(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} wajib diisi.")
    return value.strip()


def require_non_negative_int(value, field):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValidationError(
            f"{field} harus berupa bilangan bulat non-negatif."
        )
    return value


def require_positive_int(value, field):
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValidationError(
            f"{field} harus berupa bilangan bulat positif."
        )
    return value
