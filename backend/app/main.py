from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, miembros, inventario, catalogos, csv_import, dashboard, reportes
from app.routers import familias, asistencia, usuarios_gestion, roles, auditoria_router
from app.routers import iglesias, profesiones_oficios, miembros_extension, roles_eclesiasticos, grupos
from app.routers import historial_resguardos, geografia, categorias_inventario

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(miembros.router)
app.include_router(miembros_extension.router)
app.include_router(inventario.router)
app.include_router(catalogos.router)
app.include_router(csv_import.router)
app.include_router(dashboard.router)
app.include_router(reportes.router)
app.include_router(familias.router)
app.include_router(asistencia.router)
app.include_router(usuarios_gestion.router)
app.include_router(roles.router)
app.include_router(auditoria_router.router)
app.include_router(iglesias.router)
app.include_router(profesiones_oficios.router)
app.include_router(roles_eclesiasticos.router)
app.include_router(grupos.router)
app.include_router(historial_resguardos.router)
app.include_router(geografia.router)
app.include_router(categorias_inventario.router)

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["settings"] = settings
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/miembros", response_class=HTMLResponse, include_in_schema=False)
def miembros_page(request: Request):
    return templates.TemplateResponse("miembros.html", {"request": request})


@app.get("/inventario", response_class=HTMLResponse, include_in_schema=False)
def inventario_page(request: Request):
    return templates.TemplateResponse("inventario.html", {"request": request})


@app.get("/familias", response_class=HTMLResponse, include_in_schema=False)
def familias_page(request: Request):
    return templates.TemplateResponse("familias.html", {"request": request})


@app.get("/asistencia", response_class=HTMLResponse, include_in_schema=False)
def asistencia_page(request: Request):
    return templates.TemplateResponse("asistencia.html", {"request": request})


@app.get("/usuarios", response_class=HTMLResponse, include_in_schema=False)
def usuarios_page(request: Request):
    return templates.TemplateResponse("usuarios.html", {"request": request})


@app.get("/roles", response_class=HTMLResponse, include_in_schema=False)
def roles_page(request: Request):
    return templates.TemplateResponse("roles.html", {"request": request})


@app.get("/auditoria", response_class=HTMLResponse, include_in_schema=False)
def auditoria_page(request: Request):
    return templates.TemplateResponse("auditoria.html", {"request": request})


@app.get("/iglesias", response_class=HTMLResponse, include_in_schema=False)
def iglesias_page(request: Request):
    return templates.TemplateResponse("iglesias.html", {"request": request})


@app.get("/profesiones", response_class=HTMLResponse, include_in_schema=False)
def profesiones_page(request: Request):
    return templates.TemplateResponse("profesiones.html", {"request": request})


@app.get("/grupos", response_class=HTMLResponse, include_in_schema=False)
def grupos_page(request: Request):
    return RedirectResponse(url="/ministerios")

@app.get("/ministerios", response_class=HTMLResponse, include_in_schema=False)
def ministerios_page(request: Request):
    return templates.TemplateResponse("ministerios.html", {"request": request})


@app.get("/roles-eclesiasticos", response_class=HTMLResponse, include_in_schema=False)
def roles_eclesiasticos_page(request: Request):
    return templates.TemplateResponse("roles_eclesiasticos.html", {"request": request})


@app.get("/resguardos", response_class=HTMLResponse, include_in_schema=False)
def resguardos_page(request: Request):
    return templates.TemplateResponse("resguardos.html", {"request": request})


@app.get("/geografia", response_class=HTMLResponse, include_in_schema=False)
def geografia_page(request: Request):
    return templates.TemplateResponse("geografia.html", {"request": request})


@app.get("/categorias", response_class=HTMLResponse, include_in_schema=False)
def categorias_page(request: Request):
    return templates.TemplateResponse("categorias.html", {"request": request})


@app.get("/csv", response_class=HTMLResponse, include_in_schema=False)
def csv_page(request: Request):
    return templates.TemplateResponse("csv.html", {"request": request})


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
