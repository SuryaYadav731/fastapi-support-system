from fastapi import Depends, HTTPException
from app.dependencies.auth_dependencies import get_current_user


def require_role(required_roles: list):

    def role_checker(current_user=Depends(get_current_user)):

        if current_user.role not in required_roles:
            raise HTTPException(status_code=403, detail="Permission denied")

        return current_user

    return role_checker
