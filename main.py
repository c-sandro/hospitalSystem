from fastapi import FastAPI
from starlette.responses import HTMLResponse, FileResponse

from core.configs import settings
from api.v1.api_router_manager import api_router

app = FastAPI(title='Sistema Hospital')
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse('templates/redirect.html')

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                     log_level="info", reload=True)