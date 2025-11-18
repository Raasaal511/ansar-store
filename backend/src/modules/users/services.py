from fastapi import HTTPException, status


def check_user_role(user_roles: list, required_roles: list):


    if not any(role in user_roles for role in required_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для выполнения этого действия."
        )