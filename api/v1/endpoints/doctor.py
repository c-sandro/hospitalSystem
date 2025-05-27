from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.doctor_model import DoctorModel

router = APIRouter()

#POST doctor (pesquisar consultar)
def search_doctor_screen() -> FileResponse:
    return FileResponse('templates/doctors/search.html')

async def search_doctor_action(request: Request, db: AsyncSession):
    form = await request.form()

    options = form.get('options')
    param = form.get('param')

    query = None

    match options:
        #caso o parametro for nome
        case '0':
            name_list = param.split(" ")
            name_formatting = ""
            for word in name_list:
                name_formatting += word.capitalize() if len(word) > 2 else word
                name_formatting += " "

            name_formatting = name_formatting[:-1]

            query = select(DoctorModel).filter(DoctorModel.name == name_formatting)

        #caso o parametro for cpf
        case '1':
            #
            if not (param.isdigit() and param.isascii()):
                return "cpf_invalid"
            elif not check_cpf(param):
               return "cpf_invalid"
            query = select(DoctorModel).filter(DoctorModel.cpf == param)

        #caso o parametro for crm
        case '2':
            if int(param) < 1:
                return "crm_invalid"

            query = select(DoctorModel).filter(DoctorModel.crm == int(param))

        #caso o parametro for id
        case '3':
            if int(param) < 1:
                return "id_invalid"

            query = select(DoctorModel).filter(DoctorModel.id == int(param))

    async with db as session:
        result = await session.execute(query)
        doctors = result.scalars().all()

    if len(doctors) == 0:
        return "no_result"

    response_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pesquisar doutor</title>
    <link rel="stylesheet" href="/api/v1/styles">
</head>
<body>
    <div class="content">
        <b class="titleText">HOSPITAL SANTO</b> <img class="crossTitle" src="/api/v1/images/cross.png" alt="">
        <br><br>
        <h2>RESULTADO</h2> """

    formatting = '%H:%M'

    counter: int = 0

    for doctor in doctors:

        shift_start_formatted: str = doctor.shift_start.strftime(formatting)
        shift_finish_formatted: str = doctor.shift_finish.strftime(formatting)

        response_content += f"""
        <div class="searchResultDiv">
            <b>Doutor(a) {doctor.name}</b>
            <div>CPF: {doctor.cpf[:3]}.{doctor.cpf[3:6]}.{doctor.cpf[6:9]}-{doctor.cpf[9:]}</div>
            <div>CRM: {doctor.crm}</div>
            <div>Telefone: ({doctor.phone[:2]}) {doctor.phone[2:7]}-{doctor.phone[7:]}</div>
            <div>Email: {doctor.email}</div>
            <div>Horário do Turno: {shift_start_formatted}-{shift_finish_formatted}</div>
        </div>"""
        counter += 1
        if counter % 3 == 0:
            response_content += "<br>"

    response_content += """
                    <br><br>
                    <button onclick="history.back()">Fazer outra pesquisa</button>
                    <button onclick="window.location.href='/api/v1/menu'">Menu</button>
                </div>
            </body>
            </html>
            """

    return HTMLResponse(content=response_content)



def check_cpf(cpf: str) -> bool:
    cpf_verifier: int = 0

    #Soma os primeiros 9 dígitos multiplicados por 11 menos a posição deles (primeira posição = 11 - 1)
    for i in range(9):
        cpf_verifier += int(cpf[i]) * (10 - i)

    #Pega o resto da divisão
    cpf_verifier %= 11

    #Se o resto for 0 ou 1, o dígito deve ser 0
    if cpf_verifier == 0 or cpf_verifier == 1:
        cpf_verifier = 0
    #Se não, é o resto menos 11
    else:
        cpf_verifier = 11 - cpf_verifier

    #Se o décimo dígito for diferente, o CPF é inválido
    if cpf_verifier != cpf[9]:
        return False

    #Reseta para o segundo teste
    cpf_verifier = 0

    #Soma os primeiros 10 dígitos multiplicados por 12 menos a posição deles (primeira posição = 12 - 1)
    for i in range(10):
        cpf_verifier += int(cpf[i]) * (11 - i)

    # Pega o resto da divisão
    cpf_verifier %= 11

    # Se o resto for 0 ou 1, o dígito deve ser 0
    if cpf_verifier == 0 or cpf_verifier == 1:
        cpf_verifier = 0
    #Se não, é o resto menos 11
    else:
        cpf_verifier = 11 - cpf_verifier

    #Se o décimo primeiro dígito for diferente, o CPF é inválido
    if cpf_verifier != cpf[10]:
        return False

    return True