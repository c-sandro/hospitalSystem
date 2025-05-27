from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.appointment_model import AppointmentModel
from models.patient_model import PatientModel
from models.blood_type_model import BloodTypeModel
from models.patient_edit_log_model import PatientEditLogModel
from models.patient_status_log_model import PatientStatusLogModel
from schemas.patient_schema import PatientSchemaUpdated

from datetime import date, datetime

router = APIRouter()

#POST patient (criação de paciente novo)
def create_patient_screen() -> FileResponse:
    return FileResponse('templates/patients/create.html')

async def create_patient_action(request: Request, db: AsyncSession) -> str:

    form = await request.form()

    cpf = form.get("cpf")
    birth_date = form.get("birth_date")
    phone = form.get("phone")

    formatting = "%Y-%m-%d"
    birth_date_formatted = datetime.strptime(birth_date, formatting).date()

    #Validação dos dados
    if not (cpf.isdigit() and cpf.isascii()):
        return "cpf_invalid"
    elif not check_cpf(cpf):
       return "cpf_invalid"
    elif birth_date_formatted > date.today():
        return "birth_date_invalid"
    elif not (phone.isdigit() and phone.isascii()):
        return "phone_invalid"

    async with db as session:
        query = select(PatientModel).filter(PatientModel.cpf == cpf)
        result = await session.execute(query)
        unique_cpf_check = result.scalar().one_or_none()

        if unique_cpf_check:
            return "cpf_repeat"


    name_list = form.get("name").split(" ")
    name_formatting = ""
    for word in name_list:
        name_formatting += word.capitalize() if len(word) > 2 else word

    new_patient_model = PatientModel(
        name=name_formatting,
        cpf=cpf,
        birth_date=birth_date,
        sex=form.get("sex"),
        phone=phone,
        address=form.get("address"),
        email=form.get("email") if form.get("email") else None,
        blood_type_id=int(form.get("blood_type_id")) if form.get("blood_type_id") else None,
        allergies=form.get("allergies") if form.get("allergies") else None,
        status=True
    )

    async with db as session:
        session.add(new_patient_model)
        await session.commit()
        return "success"

#POST patient (busca de paciente específico)
def search_patient_screen() -> FileResponse:
    return FileResponse('templates/patients/search.html')

async def search_patient_action(request: Request, db: AsyncSession):
    form = await request.form()
    query = None

    options = form.get("options")
    param = form.get("param")

    match options:
        case '0':
            name_list = param.split(" ")
            name_formatting = ""
            for word in name_list:
                name_formatting += word.capitalize() if len(word) > 2 else word
                name_formatting += " "

            name_formatting = name_formatting[:-1]

            query = select(PatientModel).filter(PatientModel.name == name_formatting)

        case '1':
            if not (param.isdigit() and param.isascii()):
                return "cpf_invalid"
            elif not check_cpf(param):
               return "cpf_invalid"
            query = select(PatientModel).filter(PatientModel.cpf == param)

        case '2':
            if int(param) < 1:
                return "id_invalid"

            query = select(PatientModel).filter(PatientModel.id == int(param))

    async with db as session:
        result = await session.execute(query)
        patients = result.scalars().all()

    if len(patients) == 0:
        return "no_result"

    response_content = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Pesquisar paciente</title>
        <link rel="stylesheet" href="/api/v1/styles">
    </head>
    <body>
        <div class="content">
            <b class="titleText">HOSPITAL SANTO</b> <img class="crossTitle" src="/api/v1/images/cross.png" alt="">
            <br><br>
            <h2>RESULTADOS</h2>"""

    counter: int = 0
    for patient in patients:
        status: str = "Ativo" if patient.status else "Inativo"
        response_content += f"""
            <div class="searchResultDiv">
                <b>{patient.name}</b>
                <div>CPF: {patient.cpf[:3] + "." + patient.cpf[3:6] + "." + patient.cpf[6:9] + "-" + patient.cpf[9:]}</div>
                <div>ID: {patient.id}</div>
                <div>Status: {status}</div>
                <button onclick="window.location.href = '/api/v1/patients/{patient.id}'">Mais informações</button>
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
</html>"""

    response = HTMLResponse(content=response_content)

    return response

#GET patient (ver resultado da pesquisa de paciente)
async def search_patient_result_screen(patient_id: int, perm_tier: int, db: AsyncSession):
    if patient_id < 1:
        return "id_invalid"

    async with db as session:
        query = select(PatientModel).filter(PatientModel.id == patient_id)
        result = await session.execute(query)
        patient = result.scalar_one_or_none()

    if patient is None:
        return "no_result"

    async with db as session:
        query = select(BloodTypeModel).filter(BloodTypeModel.id == patient.blood_type_id)
        result = await session.execute(query)
        patient.blood_type = result.scalar_one_or_none().type if patient.blood_type_id else None

    sex: str = "Homem" if not patient.sex else "Mulher"
    email: str = "<div>Email: " + patient.email + "</div>" if patient.email else ""
    blood_type: str = "<div>Tipo Sanguíneo: " + patient.blood_type + "</div>" if patient.blood_type else ""
    allergies: str = patient.allergies if patient.allergies else "Nenhuma"
    status: str = "Ativo" if patient.status else "Inativo"

    response_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Paciente</title>
    <link rel="stylesheet" href="/api/v1/styles">
</head>
<body>
    <div class="content">
        <b class="titleText">HOSPITAL SANTO</b> <img class="crossTitle" src="/api/v1/images/cross.png" alt="">
        <br><br>
        <h2>PACIENTE</h2>
        <div>Nome: {patient.name}</div>
        <div>CPF: 
            {patient.cpf[:3]}.{patient.cpf[3:6]}.{patient.cpf[6:9]}-{patient.cpf[9:]} 
        </div>
        <div>Data de Nascimento: 
            {patient.birth_date.day}/{patient.birth_date.month}/{patient.birth_date.year}
        </div>
        <div>Status: {status}</div>
        <br>"""

    #se o usuário for recepcionista ou adm
    if perm_tier != 1:
        response_content += f"""
        <div>Telefone: ({patient.phone[:2]}) {patient.phone[2:7]}-{patient.phone[7:]}</div>
        <div>Endereço: {patient.address}</div>
        {email}
        <br>"""

    #se o usuário for doutor ou adm
    if perm_tier != 2:
        response_content += f"""
        <div>Sexo: {sex}</div>
        {blood_type}
        <div>Alergias: {allergies}</div>
        <br>"""

    #se o paciente estiver desativado, botao de reativar, e vice versa
    active_or_inactive_button = (f"""
    <button onclick="window.location.href = '/api/v1/patients/{patient_id}/deactivate'">Desativar paciente</button>
    """) if patient.status else (f"""
    <button onclick="window.location.href = '/api/v1/patients/{patient_id}/reactivate'">Reativar paciente</button>
    """)

    #se o usuário for admin, pode desativar
    active_or_inactive_button = active_or_inactive_button if perm_tier > 2 else None

    #se o usuário for recepcionista ou admin, pde editar
    edit_button = (f"""
    <button onclick="window.location.href='/api/v1/patients/{patient_id}/edit'">Editar cadastro</button>
    """) if perm_tier > 1 else ""

    response_content += (f"""
        {edit_button}
        {active_or_inactive_button}
        <br><br>
        <button onclick="history.back()">Ver outro paciente</button>
        <button onclick="window.location.href='/api/v1/menu'">Menu</button>
    </div>
</body>
</html>""")

    response = HTMLResponse(content=response_content)

    return response

#PUT patient (atualizar dados do paciente da pesquisa)
def edit_patient_screen() -> FileResponse:
    return FileResponse('templates/patients/edit.html')

async def edit_patient_action(user_system_id: int, patient_id: int, request: Request, db: AsyncSession) -> str:
    if patient_id < 1:
        return "id_invalid"

    async with db as session:
        query = select(PatientModel).filter(PatientModel.id == patient_id)
        result = await session.execute(query)
        patient = result.scalar_one_or_none()

    if patient is None:
        return "no_result"

    form = await request.form()

    birth_date = form.get("birth_date")
    phone = form.get("phone")

    if birth_date:
        if birth_date > date.today():
            return "birth_date_invalid"
    if phone:
        if not (phone.isdigit() and phone.isascii()):
            return "phone_invalid"

    edit_patient_input = PatientSchemaUpdated(
        name=form.get("name"),
        birth_date=birth_date if birth_date else None,
        sex=form.get("sex") if form.get("sex") else None,
        phone=phone,
        address=form.get("address"),
        email=form.get("email") if form.get("email") else None,
        blood_type_id=int(form.get("blood_type_id")) if form.get("blood_type_id") else None,
        allergies=form.get("allergies")
    )

    async with db as session:
        query = select(PatientModel).filter(PatientModel.id == patient_id)
        result = await session.execute(query)
        patient_up = result.scalar_one_or_none()

        changes: str = ""

        changes, patient_up = await create_edit_log(edit_patient_input, patient_up, session)

        new_patient_edit_log = PatientEditLogModel(
            date_time=datetime.now(),
            user_system_id=user_system_id,
            patient_id=patient_id,
            changes=changes
        )
        session.add(new_patient_edit_log)
        await session.commit()

        return "success"

def deactivate_patient_screen():
    return FileResponse('templates/patients/deactivate.html')

def reactivate_patient_screen():
    return FileResponse('templates/patients/reactivate.html')

async def change_status_patient_action(patient_id: int, user_id: int, activating: bool, request: Request, db: AsyncSession):
    form = await request.form()

    if patient_id < 1:
        return "id_invalid"

    async with db as session:
        query = select(PatientModel).filter(PatientModel.id == patient_id)
        result = await session.execute(query)
        patient = result.scalar_one_or_none()

    if patient is None:
        return "no_result"

    if not activating and not patient.status:
        return "already_deactivated"
    elif activating and patient.status:
        return "already_activated"

    async with db as session:
        query = select(AppointmentModel).filter(AppointmentModel.patient_id == patient.id)
        result = await session.execute(query)
        appointments = result.scalars().all()

    if len(appointments) != 0:
        for appoint in appointments:
            if appoint.date_time > datetime.now():
                return "is_occupied"

    new_patient_log = PatientStatusLogModel(
        date_time=datetime.now(),
        user_system_id=user_id,
        patient_id=patient.id,
        reason=form.get("reason"),
        new_status=not patient.status
    )

    async with db as session:
        query = select(PatientModel).filter(PatientModel.id == patient_id)
        result = await session.execute(query)
        patient = result.scalar_one_or_none()

        patient.status = not patient.status

        session.add(new_patient_log)

        await session.commit()
        return "success"

# --- FUNÇÕES GENÉRICAS ---

async def create_edit_log(edit_patient_input: PatientSchemaUpdated, patient_up: PatientModel, session: AsyncSession):
    changes: str = ""

    if edit_patient_input.name and patient_up.name != edit_patient_input.name:
        changes += f"Nome: de {patient_up.name} para {edit_patient_input.name}; "
        patient_up.name = edit_patient_input.name

    if edit_patient_input.birth_date and patient_up.birth_date != edit_patient_input.birth_date:
        changes += f"Data de nascimento: de {patient_up.birth_date} para {edit_patient_input.birth_date}; "
        patient_up.birth_date = edit_patient_input.birth_date

    if edit_patient_input.sex and patient_up.sex != edit_patient_input.sex:
        sex_up: str = "Homem" if not patient_up.sex else "Mulher"
        edit_sex: str = "Homem" if not edit_patient_input.sex else "Mulher"
        changes += f"Sexo: de {sex_up} para {edit_sex}; "
        patient_up.sex = edit_patient_input.sex

    if edit_patient_input.phone and patient_up.phone != edit_patient_input.phone:
        changes += f"Telefone: de {patient_up.phone} para {edit_patient_input.phone}; "
        patient_up.phone = edit_patient_input.phone

    if edit_patient_input.address and patient_up.address != edit_patient_input.address:
        changes += f"Endereço: de {patient_up.address} para {edit_patient_input.address}; "
        patient_up.address = edit_patient_input.address

    if edit_patient_input.email and patient_up.email != edit_patient_input.email:
        changes += f"Email: de {patient_up.email} para {edit_patient_input.email}; "
        patient_up.email = edit_patient_input.email

    if edit_patient_input.blood_type_id and patient_up.blood_type_id != edit_patient_input.blood_type_id:
        query = select(BloodTypeModel).filter(BloodTypeModel.id == patient_up.blood_type_id)
        result = await session.execute(query)
        blood_type_up = result.scalar_one_or_none().type if patient_up.blood_type_id else ""

        query = select(BloodTypeModel).filter(BloodTypeModel.id == edit_patient_input.blood_type_id)
        result = await session.execute(query)
        edit_blood_type = result.scalar_one_or_none().type

        changes += f"Tipo sanguíneo: de {blood_type_up} para {edit_blood_type}; "
        patient_up.blood_type_id = edit_patient_input.blood_type_id

    if edit_patient_input.allergies and patient_up.name != edit_patient_input.name:
        changes += f"Nome: de {patient_up.name} para {edit_patient_input.name}; "
        patient_up.allergies = edit_patient_input.allergies

    return changes, patient_up

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