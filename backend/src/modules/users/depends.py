from fastapi import Depends


def role_deps(*required_roles: str):
    """
    Заглушка для проверки ролей.
    В реальном приложении здесь должна быть логика проверки JWT токена и ролей пользователя.
    """
    def dependency():
        # TODO: Реализовать проверку JWT токена и ролей
        pass
    return Depends(dependency)

