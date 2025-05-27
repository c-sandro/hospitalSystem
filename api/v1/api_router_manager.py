from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse

from sqlalchemy.ext.asyncio import AsyncSession

from core.configs import settings
from core.deps import get_session

from api.v1.endpoints import menu, patient, appointment, doctor, user_system

api_router = APIRouter()

current_user_id: int = -1
current_user_perm_tier: int = 0

# --- PÁGINAS DE MENU ---

#GET user_system (logar no sistema)
@api_router.get("/login", response_class=FileResponse)
def login_screen():
    return menu.login_screen()
@api_router.post("/login", response_class=FileResponse)
async def login_action(request: Request, db: AsyncSession = Depends(get_session)):

    #pegar o resultado da função e, se der certo, guardar os parametros globalmente e ir para o menu
    global current_user_id
    global current_user_perm_tier
    response, current_user_id, current_user_perm_tier = await menu.login_action(request, db)

    if response == "login_fail":
        return return_error(status.HTTP_404_NOT_FOUND, "Email ou senha incorretos")

    return response

#Tela de menu
@api_router.get("/menu", response_class=FileResponse)
async def menu_screen():
    global current_user_perm_tier

    #menus diferentes para cada tier de permissão
    match current_user_perm_tier:
        case 1:
            return FileResponse('templates/menu_doctor.html', status.HTTP_200_OK)
        case 2:
            return FileResponse('templates/menu_recept.html', status.HTTP_200_OK)
        case 3:
            return FileResponse('templates/menu_admin.html', status.HTTP_200_OK)

    return return_error(status.HTTP_401_UNAUTHORIZED,"Você precisa logar para acessar essa página")


# --- PÁGINAS DE PACIENTE ---

#POST patient (criação de paciente novo)
@api_router.get('/patients/create', response_class=FileResponse)
def create_patient_screen():
    #função presente em todas as chamadas de página para garantir que o usuário possua permissão de acesso sempre
    if check_perm_access(2):
        return check_perm_access(2)

    return patient.create_patient_screen()
@api_router.post('/patients/create', response_class=FileResponse)
async def create_patient_action(request: Request, db: AsyncSession = Depends(get_session)):
    if check_perm_access(2):
        return check_perm_access(2)

    function_result: str = await patient.create_patient_action(request, db)

    #eu to fazendo essas listas de casos para fazer testes de excessão mais rapidamente, de maneira mais compacta e
    #pra poder adicionar e remover excessões mais rapidamente
    cases = ["cpf_invalid", "birth_date_invalid", "phone_invalid", "cpf_repeat"]
    func_params1 = [status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST,
                    status.HTTP_400_BAD_REQUEST, "Paciente criado com sucesso"]
    func_params2 = ["CPF inválido", "Data de nascimento inválida", "Telefone inválido",
                    "CPF ja está cadastrado", "Criar outro paciente"]

    return check_result(function_result, cases, func_params1, func_params2)

#GET patient (busca de paciente específico)
@api_router.get('/patients/search', response_class=FileResponse)
def search_patient_screen():
    if check_perm_access(0):
        return check_perm_access(0)

    return patient.search_patient_screen()
@api_router.post('/patients/search', response_class=HTMLResponse)
async def search_patient_action(request: Request, db: AsyncSession = Depends(get_session)):
    if check_perm_access(0):
        return check_perm_access(0)

    function_result = await patient.search_patient_action(request, db)

    cases = ["cpf_invalid", "id_invalid", "no_result"]
    func_params1 = [status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST,
                    status.HTTP_404_NOT_FOUND, "Paciente criado com sucesso"]
    func_params2 = ["CPF inválido", "ID inválido", "Nenhum paciente foi encontrado", "Criar outro paciente"]

    return check_result(function_result, cases, func_params1, func_params2)
@api_router.get('/patients/{patient_id}', response_class=HTMLResponse)
async def search_patient_result_screen(patient_id: int, db: AsyncSession = Depends(get_session)):
    if check_perm_access(0):
        return check_perm_access(0)

    function_result = await patient.search_patient_result_screen(patient_id, current_user_perm_tier, db)

    cases = ["id_invalid", "no_result"]
    func_params1 = [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND, "Paciente criado com sucesso"]
    func_params2 = ["ID inválido", "Nenhum paciente foi encontrado", "Criar outro paciente"]

    return check_result(function_result, cases, func_params1, func_params2)

#PUT patient (atualizar dados do paciente da pesquisa)
@api_router.get('/patients/{patient_id}/edit', response_class=FileResponse)
def edit_patient_screen(patient_id: int):
    if check_perm_access(2):
        return check_perm_access(2)

    return patient.edit_patient_screen()
@api_router.post('/patients/{patient_id}/edit', response_class=FileResponse)
async def edit_patient_action(patient_id: int, request: Request, db: AsyncSession = Depends(get_session)):
    if check_perm_access(2):
        return check_perm_access(2)

    function_result: str = await patient.edit_patient_action(current_user_id, patient_id, request, db)

    cases = ["id_invalid", "birth_date_invalid", "phone_invalid", "no_result"]
    func_params1 = [status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST,
                    status.HTTP_404_NOT_FOUND, "Paciente editado com sucesso"]
    func_params2 = ["ID inválido", "Data de nascimento inválida", "Telefone inválido",
                    "Nenhum paciente com este ID", "Fazer outra edição"]

    return check_result(function_result, cases, func_params1, func_params2)

#PUT patient (desativar/ativar paciente)
@api_router.get('/patients/{patient_id}/deactivate', response_class=FileResponse)
def deactivate_patient_screen():
    if check_perm_access(3):
        return check_perm_access(3)

    return patient.deactivate_patient_screen()
@api_router.post('/patients/{patient_id}/deactivate', response_class=FileResponse)
async def deactivate_patient_action(patient_id: int, request: Request, db: AsyncSession = Depends(get_session)):
    if check_perm_access(3):
        return check_perm_access(3)

    function_result: str = await patient.change_status_patient_action(patient_id, current_user_id, False, request, db)

    cases = ["id_invalid", "already_deactivated", "is_occupied", "no_result"]
    func_params1 = [status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST,
                    status.HTTP_404_NOT_FOUND, "Paciente desativado com sucesso"]
    func_params2 = ["ID inválido", "Paciente ja está desativado", "Paciente possui consultas pendentes",
                    "Nenhum paciente com este ID", "Desativar outra conta"]

    return check_result(function_result, cases, func_params1, func_params2)

@api_router.get('/patients/{patient_id}/reactivate', response_class=FileResponse)
def deactivate_patient_screen():
    if check_perm_access(3):
        return check_perm_access(3)

    return patient.reactivate_patient_screen()
@api_router.post('/patients/{patient_id}/reactivate', response_class=FileResponse)
async def deactivate_patient_action(patient_id: int, request: Request, db: AsyncSession = Depends(get_session)):
    if check_perm_access(3):
        return check_perm_access(3)

    function_result: str = await patient.change_status_patient_action(patient_id, current_user_id, True, request, db)

    cases = ["id_invalid", "already_deactivated", "is_occupied", "no_result"]
    func_params1 = [status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST,
                    status.HTTP_404_NOT_FOUND, "Paciente reativado com sucesso"]
    func_params2 = ["ID inválido", "Paciente ja está ativado", "Paciente possui consultas pendentes",
                    "Nenhum paciente com este ID", "Reativar outra conta"]

    return check_result(function_result, cases, func_params1, func_params2)


# --- PÁGINAS DE CONSULTA ---

#POST appointment (criar consulta baseado em um cliente)
@api_router.get('/appointments/create', response_class=FileResponse)
def create_appointment_screen():
    if check_perm_access(2):
        return check_perm_access(2)

    return appointment.create_appointment_screen()
@api_router.post('/appointments/create', response_class=HTMLResponse)
async def create_appointment_action(request: Request, db: AsyncSession = Depends(get_session)):
    if check_perm_access(2):
        return check_perm_access(2)

    function_result = await appointment.create_appointment_action(request, db)

    cases = ["patient_cpf_invalid", "patient_no_result", "doctor_no_result"]
    func_params1 = [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND, status.HTTP_404_NOT_FOUND]
    func_params2 = ["CPF do paciente inválido", "Nenhum paciente foi encontrado", "Nenhum doutor foi encontrado"]

    return check_result(function_result, cases, func_params1, func_params2)
@api_router.post('/appointments/create/confirm', response_class=FileResponse)
async def create_appointment_finish(request: Request, db: AsyncSession = Depends(get_session)):
    if check_perm_access(2):
        return check_perm_access(2)

    function_result = await appointment.create_appointment_finish(request, db)

    cases = ["patient_id_invalid", "doctor_id_invalid", "date_time_invalid", "patient_no_result",
             "doctor_no_result", "patient_inactive", "doctor_out_of_shift", "pat_time_not_available",
             "doc_time_not_available"]
    func_params1 = [status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST,
                    status.HTTP_404_NOT_FOUND, status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST,
                    status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST,
                    "Consulta criada com sucesso"]
    func_params2 = ["ID do paciente inválido", "ID do doutor inválido", "Data da consulta invalida",
                    "Nenhum paciente foi encontrado", "Nenhum doutor foi encontrado", "Paciente recebido está inativo",
                    "Doutor fora de turno no horário", "Horário do paciente já está ocupado",
                    "Horário do doutor já está ocupado", "Criar outra consulta"]

    return check_result(function_result, cases, func_params1, func_params2)

#GET appointment (pesquisar consultas)
@api_router.get('/appointments/search', response_class=FileResponse)
def search_appointment_screen():
    if check_perm_access(2):
        return check_perm_access(2)

    return appointment.search_appointment_screen()
@api_router.post('/appointments/search', response_class=HTMLResponse)
async def search_appointment_action(request: Request, db: AsyncSession = Depends(get_session)):
    if check_perm_access(2):
        return check_perm_access(2)

    function_result = await appointment.search_appointment_action(request, db)

    cases = ["appoint_id_invalid", "patient_cpf_invalid", "doctor_crm_invalid",
             "appoint_no_result", "patient_no_result", "doctor_no_result"]
    func_params1 = [status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST,
                    status.HTTP_404_NOT_FOUND, status.HTTP_404_NOT_FOUND, status.HTTP_404_NOT_FOUND]
    func_params2 = ["ID da consulta inválido", "CPF do paciente inválido", "CRM do doutor inválido",
                    "Nenhuma consulta foi encontrada", "Nenhum paciente foi encontrado", "Nenhum doutor foi encontrado"]

    return check_result(function_result, cases, func_params1, func_params2)


# --- PÁGINAS DE ADMIN ---

#GET doctor (pesquisar paciente)
@api_router.get('/doctors/search', response_class=FileResponse)
def search_doctor_screen():
    if check_perm_access(3):
        return check_perm_access(3)

    return doctor.search_doctor_screen()
@api_router.post('/doctors/search', response_class=HTMLResponse)
async def search_doctor_action(request: Request, db: AsyncSession = Depends(get_session)):
    if check_perm_access(3):
        return check_perm_access(3)

    function_result = await doctor.search_doctor_action(request, db)

    cases = ["cpf_invalid", "crm_invalid", "id_invalid", "no_result"]
    func_params1 = [status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST,
                    status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
    func_params2 = ["CPF do doutor inválido", "CRM do doutor inválido",
                    "ID do doutor inválido", "Nenhum doutor foi encontrado"]

    return check_result(function_result, cases, func_params1, func_params2)

#GET user_system (pesquisar usuário do sistema)
@api_router.get('/users/search', response_class=FileResponse)
def search_user_screen():
    if check_perm_access(3):
        return check_perm_access(3)

    return user_system.search_user_screen()
@api_router.post('/users/search', response_class=HTMLResponse)
async def search_user_action(request: Request, db: AsyncSession = Depends(get_session)):
    if check_perm_access(3):
        return check_perm_access(3)

    function_result = await user_system.search_user_action(request, db)

    cases = ["id_invalid", "no_result"]
    func_params1 = [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
    func_params2 = ["ID do usuário inválido", "Nenhum usuário foi encontrado"]

    return check_result(function_result, cases, func_params1, func_params2)


# --- PÁGINAS GENÉRICAS ---

#GET images (pegar imagens)
@api_router.get('/images/{name}', response_class=FileResponse)
def get_images(name: str):
    return FileResponse(f'templates/images/{name}')

#GET styles (pegar o css)
@api_router.get('/styles', response_class=FileResponse)
def get_styles():
    return FileResponse('templates/css/styles.css')

#GET js (pegar o javascript)
@api_router.get('/js', response_class=FileResponse)
def get_script():
    return FileResponse('templates/js/main.js')

#Telas de erro
@api_router.get("/error", response_class=FileResponse)
async def error_screen():
    return FileResponse('templates/generic/error.html', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_router.post("/error", response_class=FileResponse)
async def error_screen():
    return FileResponse('templates/generic/error.html', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def return_error(status: str, desc: str):
    return RedirectResponse(url=f"{settings.API_V1_STR}/error?error={status}&desc={desc}")

#Telas de sucesso
@api_router.get("/success", response_class=FileResponse)
async def success_screen():
    return FileResponse('templates/generic/success.html', status_code=status.HTTP_200_OK)
@api_router.post("/success", response_class=FileResponse)
async def success_screen():
    return FileResponse('templates/generic/success.html', status_code=status.HTTP_200_OK)

def return_success(desc: str, button: str):
    return RedirectResponse(url=f"{settings.API_V1_STR}/success?desc={desc}&button={button}")

# --- FUNÇÕES GENÉRICAS ---

def check_perm_access(perm_check: int):
    global current_user_perm_tier
    if current_user_perm_tier == 0:
        return return_error(status.HTTP_401_UNAUTHORIZED, "Você precisa logar para acessar")
    elif current_user_perm_tier < perm_check:
        return return_error(status.HTTP_403_FORBIDDEN, "Você não possui acesso para acessar essa página")

def check_result(function_result, cases, func_params1, func_params2):

    cont: int = 0

    for case in cases:
        if function_result == case:
            return return_error(func_params1[cont], func_params2[cont])
        cont += 1

    if function_result == "success":
        return return_success(func_params1[cont], func_params2[cont])

    return function_result