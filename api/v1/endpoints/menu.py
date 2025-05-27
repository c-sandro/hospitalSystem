from fastapi import HTTPException, status, Request
from fastapi.responses import FileResponse

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from core.deps import authenticate_member

def login_screen():
    return FileResponse('templates/login.html', status_code=status.HTTP_200_OK)

async def login_action(request: Request, db: AsyncSession):
    form = await request.form()
    user_system = await authenticate_member(form.get("email"), form.get("password"), db)
    if not user_system:
        return "login_fail", None, None

    response = RedirectResponse('./menu', headers={"Method": "GET"}, status_code=status.HTTP_302_FOUND)

    match user_system.permission_tier:
        case 1:
            response.path = 'templates/menu_doctor.html'
        case 2:
            response.path = 'templates/menu_recept.html'
        case 3:
            response.path = 'templates/menu_admin.html'

    return response, user_system.id, user_system.permission_tier
