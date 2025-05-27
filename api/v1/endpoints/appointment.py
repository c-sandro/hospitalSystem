from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.appointment_model import AppointmentModel
from models.doctor_model import DoctorModel
from models.patient_model import PatientModel
from datetime import datetime, timedelta

router = APIRouter()

#POST appointment (criar consulta baseado em um cliente)
def create_appointment_screen() -> FileResponse:
    return FileResponse('templates/appointments/create.html')

async def create_appointment_action(request: Request, db: AsyncSession) -> str:
    form = await request.form()
    query = None

    patient_options = form.get("patient_options")
    patient_param = form.get("patient_param")
    doctor_name = form.get("doctor_name")

    match patient_options:
        #se o parametro for nome
        case "0":
            name_list = patient_param.split(" ")
            name_formatting = ""
            for word in name_list:
                name_formatting += word.capitalize() if len(word) > 2 else word

            query = select(PatientModel).filter(PatientModel.name == name_formatting)

        #se o parametro for cpf
        case "1":
            #se o cpf nao for somente digitos e se o cpf nao seguir as regras de cpf
            if not (patient_param.isdigit() and patient_param.isascii()):
                return "patient_cpf_invalid"
            elif not check_cpf(patient_param):
                return "cpf_invalid"
            query = select(PatientModel).filter(PatientModel.cpf == patient_param)

    async with db as session:
        #pesquisar paciente baseado no parametro
        result = await session.execute(query)
        patients = result.scalars().all()

        name_list = doctor_name.split(" ")
        name_formatting = ""
        for word in name_list:
            name_formatting += word.capitalize() if len(word) > 2 else word
            name_formatting += " "

        name_formatting = name_formatting[:-1]

        #pesquisar doutor baseado no nome
        query = select(DoctorModel).filter(DoctorModel.name == name_formatting)
        result = await session.execute(query)
        doctors = result.scalars().all()

    #se nenhum paciente for achado
    if len(patients) == 0:
        return "patient_no_result"

    #se nenhum doutor for achado
    if len(doctors) == 0:
        return "doctor_no_result"

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
        <h2>RESULTADOS</h2>
        <div class="appointmentResultContainer">
            <div class="appointmentResultChild">
                <h3>Pacientes</h3>"""

    counter: int = 0

    for patient in patients:
        #adicionar os pacientes na página
        status: str = "Ativo" if patient.status else "Inativo"
        response_content += f"""
                <div class="searchResultDiv">
                    <b>{patient.name}</b>
                    <div>CPF: {patient.cpf[:3]}.{patient.cpf[3:6]}.{patient.cpf[6:9]}-{patient.cpf[9:]}</div>
                    <div>ID: {patient.id}</div>
                    <div>Status: {status}</div>
                </div>"""

        #a cada 2 pacientes, quebrar a linha
        counter += 1
        if counter % 2 == 0:
            response_content += "<br>"

    response_content += "<br><h3>Doutores</h3>"

    formatting: str = '%H:%M'

    for doctor in doctors:

        #formatar o horário do turno pra HH:MM
        doc_shift_start_formatted: str = doctor.shift_start.strftime(formatting)
        doc_shift_finish_formatted: str = doctor.shift_finish.strftime(formatting)

        #adicionar os doutores na página
        response_content += f"""
                <div class="searchResultDiv">
                    <b>{doctor.name}</b>
                    <div>CPF: {doctor.cpf[:3] + "." + doctor.cpf[3:6] + "." + doctor.cpf[6:9] + "-" + doctor.cpf[9:]}</div>
                    <div>CRM: {doctor.crm}</div>
                    <div>Inicio do turno: {doc_shift_start_formatted} | Fim do turno: {doc_shift_finish_formatted}</div>
                    <div>ID: {doctor.id}</div>
                </div><br>"""

    response_content += f"""
            </div>
            <div class="appointmentResultChild">
                <h3>Dados da Consulta:</h3>
                <form action="./create/confirm" method="post">
                    <div class="patient_id-getter">
                        <label for="patient_id">ID do paciente:</label>
                        <input type="number" id="patient_id" name="patient_id" required> <label class="redAsteriskText">*</label>
                    </div>
                    <br>
                    <div class="doctor_id-getter">
                        <label for="doctor_id">ID do doutor:</label>
                        <input type="number" id="doctor_id" name="doctor_id" required> <label class="redAsteriskText">*</label>
                    </div>
                    <br>
                    <div class="date_time-getter">
                        <label for="date_time">Data e hora da consulta (ocupa 30min do horário do doutor):</label><br>
                        <input type="datetime-local" id="date_time" name="date_time" required> <label class="redAsteriskText">*</label>
                    </div>
                    <br>
                    <label class="redAsteriskText">*</label> = Obrigatório |
                    <input type="submit" value="Confirmar"> 
                    <br>
                    <button onclick="history.back()">Voltar</button>
                    <button onclick="window.location.href='/api/v1/menu'">Menu</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>"""

    return HTMLResponse(content=response_content)

async def create_appointment_finish(request: Request, db: AsyncSession) -> str:
    form = await request.form()

    patient_id = form.get('patient_id')
    doctor_id = form.get('doctor_id')
    date_time = form.get('date_time')

    #se o id for 0 ou menos (inválido)
    if int(patient_id) < 1:
        return "patient_id_invalid"

    #se o id for 0 ou menos (inválido)
    if int(doctor_id) < 1:
        return "doctor_id_invalid"

    #pegar o texto e transformar em datetime
    formatting: str = '%Y-%m-%dT%H:%M'
    date_time_converted = datetime.strptime(date_time, formatting)

    #se a data for para o passado
    if timedelta(date_time_converted <= datetime.now()):
        return "date_time_invalid"

    async with db as session:
        #pegar os pacientes baseado no id
        query = select(PatientModel).filter(PatientModel.id == int(patient_id))
        result = await session.execute(query)
        patient = result.scalar_one_or_none()

        #pegar os doutores baseado no id
        query = select(DoctorModel).filter(DoctorModel.id == int(doctor_id))
        result = await session.execute(query)
        doctor = result.scalar_one_or_none()

    if patient is None:
        return "patient_no_result"

    if doctor is None:
        return "doctor_no_result"

    #se o paciente for inativo
    if not patient.status:
        return "patient_inactive"

    #se a data for fora do turno do doutor
    if not (doctor.shift_start < date_time_converted.time() < doctor.shift_finish):
        return "doctor_out_of_shift"

    async with db as session:
        #pegar as consultas do doutor
        query = select(AppointmentModel).filter(doctor.id == AppointmentModel.doctor_id)
        result = await session.execute(query)
        doc_appointments = result.scalars().all()

        #pegar as consultas do paciente
        query = select(AppointmentModel).filter(patient.id == AppointmentModel.patient_id)
        result = await session.execute(query)
        pat_appointments = result.scalars().all()

    for appoint in pat_appointments:
        #se a consulta for no meio de outra consulta
        if appoint.date_time <= date_time_converted <= appoint.date_time + timedelta(minutes=30):
            return "pat_time_not_available"

    for appoint in doc_appointments:
        #se a consulta for no meio de outra consulta
        if appoint.date_time <= date_time_converted <= appoint.date_time + timedelta(minutes=30):
            return "doc_time_not_available"

    new_appointment = AppointmentModel(
        patient_id=int(patient_id),
        doctor_id=int(doctor_id),
        date_time=date_time_converted
    )

    async with db as session:
        session.add(new_appointment)
        await session.commit()
        return "success"

#GET appointment (pesquisar consultas)
def search_appointment_screen() -> FileResponse:
    return FileResponse('templates/appointments/search.html')

async def search_appointment_action(request: Request, db: AsyncSession):
    form = await request.form()

    options = form.get('options')
    param = form.get('param')

    query = None

    match options:
        #se o parametro for id
        case "0":
            if int(param) < 1:
                return "appoint_id_invalid"

            query = select(AppointmentModel).filter(AppointmentModel.id == int(param))

        #se o parametro for cpf do paciente
        case "1":
            #se o cpf nao for somente digitos e se o cpf nao seguir as regras de cpf
            if not (param.isdigit() and param.isascii()):
                return "patient_cpf_invalid"
            elif not check_cpf(form.get("param")):
                return "cpf_invalid"

            async with db as session:
                query = select(PatientModel).filter(PatientModel.cpf == param)
                result = await session.execute(query)
                patient = result.scalar_one_or_none()

            if patient is None:
                return "patient_no_result"

            query = select(AppointmentModel).filter(AppointmentModel.patient_id == patient.id)

        #se o parametro for crm do doutor
        case "2":
            if int(param) < 1:
                return "doctor_crm_invalid"

            async with db as session:
                query = select(DoctorModel).filter(DoctorModel.crm == int(param))
                result = await session.execute(query)
                doctor = result.scalar_one_or_none()

            if doctor is None:
                return "doctor_no_result"

            query = select(AppointmentModel).filter(AppointmentModel.doctor_id == doctor.id)

    async with db as session:
        result = await session.execute(query)
        appointments = result.scalars().all()

    #se não houver nenhuma consulta
    if len(appointments) == 0:
        return "appoint_no_result"

    response_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pesquisar consulta</title>
    <link rel="stylesheet" href="/api/v1/styles">
</head>
<body>
    <div class="content">
        <b class="titleText">HOSPITAL SANTO</b> <img class="crossTitle" src="/api/v1/images/cross.png" alt="">
        <br>
        <h2>RESULTADOS</h2>"""

    counter: int = 0

    for appoint in appointments:

        #pegar o paciente e o doutor da consulta
        async with db as session:
            query = select(DoctorModel).filter(DoctorModel.id == appoint.doctor_id)
            result = await session.execute(query)
            doctor = result.scalar_one_or_none()

            query = select(PatientModel).filter(PatientModel.id == appoint.patient_id)
            result = await session.execute(query)
            patient = result.scalar_one_or_none()

        #formatar a hora para HH:MM e definir o fim da consulta para 30min depois do começo
        formatting = '%H:%M'
        appoint_time_start_formatted: str = appoint.date_time.time().strftime(formatting)
        appoint_time_finish: datetime = appoint.date_time + timedelta(minutes=30)
        appoint_time_finish_formatted: str = appoint_time_finish.time().strftime(formatting)

        #formatar a hora pata DD/MM/AAAA
        formatting = '%d/%m/%Y'
        appoint_date_formatted: str = appoint.date_time.date().strftime(formatting)

        response_content += f"""
        <div class="searchResultDiv">
            <b>Consulta N°{appoint.id}</b>
            <div>Nome do Paciente: {patient.name}</div>
            <div>Nome do Doutor: {doctor.name}</div>
            <div>Data da Consulta: {appoint_date_formatted}</div>
            <div>Horário da Consulta: {appoint_time_start_formatted}-{appoint_time_finish_formatted}</div>
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