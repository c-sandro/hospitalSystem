from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_system_model import UserSystemModel

router = APIRouter()

#GET user_system (pesquisar usuário)
def search_user_screen() -> FileResponse:
    return FileResponse('templates/users/search.html')

async def search_user_action(request: Request, db: AsyncSession):
    form = await request.form()

    options = form.get('options')
    param = form.get('param')

    query = None

    match options:
        case '0':
            query = select(UserSystemModel).filter(UserSystemModel.email == param)

        case '1':
            if int(param) < 1:
                return "id_invalid"

            query = select(UserSystemModel).filter(UserSystemModel.id == int(param))

    async with db as session:
        result = await session.execute(query)
        users = result.scalars().all()

    if len(users) == 0:
        return "no_result"

    response_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pesquisar usuários</title>
    <link rel="stylesheet" href="/api/v1/styles">
</head>
<body>
    <div class="content">
        <b class="titleText">HOSPITAL SANTO</b> <img class="crossTitle" src="/api/v1/images/cross.png" alt="">
        <br><br>
        <h2>RESULTADO</h2>"""

    counter: int = 0

    for user in users:

        response_content += f"""
        <div class="searchResultDiv">
            <b>Usuário N°{user.id}</b>
            <div>Email: {user.email}</div>
            <div>Tier de Permissão: {user.permission_tier}</div>
        </div>"""

        counter += 1
        if counter % 3 == 0:
            response_content += "<br>"

    response_content += """
        <br>
        <button onclick="history.back()">Fazer outra pesquisa</button>
        <button onclick="window.location.href='/api/v1/menu'">Menu</button>
    </div>
</body>
</html>"""

    return HTMLResponse(content=response_content)