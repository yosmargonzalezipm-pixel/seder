# SEDER — Sistema de Administración Eclesial

## Identidad y Rol
Sistema de Administración para Iglesia (SEDER) construido con Python/FastAPI, MySQL, Docker y frontend web vanilla JS. El sistema gestiona miembros, inventario, asistencia, familias, ministerios, usuarios, roles e iglesias, con carga masiva CSV, reportes Excel/PDF y dashboard estadístico.

- **Idioma:** Español (código, comentarios, UI)
- **Tono técnico y directo**

## Stack Tecnológico
- **Backend:** Python 3.11+ / FastAPI / SQLAlchemy / Jinja2 / bcrypt 4.1.3
- **DB:** MySQL 8.0 en Docker (puerto 3307 host)
- **Frontend:** Tailwind CSS via CDN, SPA vanilla JS
- **Contenedores:** Docker Compose v1.29.2 (comando: `docker-compose` con guión)
- **Autenticación:** JWT + bcrypt con passlib

## Accesos
- Backend API: http://localhost:8086
- Login: admin / admin123
- phpMyAdmin: http://localhost:8085 (pendiente de levantar — imagen `phpmyadmin:5.2`)

## Convenciones de Código

### Permisos
- Formato: `{modulo}.{accion}` (ej: `miembros.ver`, `ministerios.crear`)
- Sidebar filtra módulos con `permisos.some(p => p.startsWith(key))`
- Rol "Administrador" (ID 1) bypassa verificaciones
- Roles eclesiásticos (IDs ≥ 4) en tabla `Roles` sin permisos de sistema

### Backend
- Routers registrados en `main.py` con `APIRouter(prefix="/api/{modulo}")`
- Schemas Pydantic: `*Out`, `*Create`, `*Update` por módulo
- Permiso check: `tiene_permiso(usuario, "modulo.accion", db)`
- Catálogos: iglesias usa `SelectOption` (value/label), profesiones/oficios usan `CatalogoOut` (ID/Nombre)

### Frontend
- Módulos en `ALL_MODULES`: key, label, icono, grupo (personas|recursos|organizacion|sistema), ruta
- Profesiones/Oficios multi-select via `PUT /api/miembros/{id}/profesiones` y `.../oficios`
- Miembro `ID_Ciudad` e `ID_Parroquia` NOT NULL — default `1` si no se selecciona
- PDFs con `Content-Disposition: inline`, descarga via fetch + blob + window.open
- Dashboard stats/reports ocultos por defecto (toggle show/hide)

### Base de Datos
- Schema en `db/init.sql` (sincronizado con `seder.sql`)
- Columnas en español con prefijo `ID_` para claves
- `Estado_Asistencia` usa `String(20)` en SQLAlchemy (no SAEnum)
- Seed data: 3 roles, 28+ permisos, datos de referencia

## Decisiones Clave
- `Miembro` en `miembro.py` (no en `usuario.py`) para evitar duplicación de tabla SQLAlchemy
- phpMyAdmin usa `phpmyadmin:5.2` (imagen más pequeña, evita `latest`)
- bcrypt 4.1.3 pinneado para compatibilidad con passlib
- `/grupos` redirige a `/ministerios` con 307 (permisos renombrados de `grupos.*` a `ministerios.*`)
- Logo físico (`logoDiosesamor.jpg`) en `/static/` pero no se usa; se muestra texto "Dios es Amor / 1 Juan 4:8"

## Comandos Útiles
```bash
docker-compose up -d                    # Levantar servicios
docker-compose restart backend          # Reiniciar backend tras cambios
docker-compose down                     # Bajar servicios
docker-compose exec -T mysql mysql ...  # Consultas directas a MySQL
docker-compose logs -f backend          # Logs del backend
```

## Estado Actual
- 18 routers registrados, 15 templates HTML, todos los CRUD implementados:
  - Miembros (con profesiones/oficios multi-select)
  - Inventario (con columna "Resguardo" y botón "Ver")
  - Familias, Asistencia, Usuarios, Roles, Iglesias
  - Profesiones, Oficios, Roles Eclesiásticos
  - Ministerios (con selector de rol al agregar miembro)
  - Historial de Resguardos (página propia + acceso desde inventario)
  - Carga masiva CSV (miembros + inventario)
  - Reportes Excel/PDF con preview modal
  - Dashboard con sidebar lateral oscuro, módulos agrupados, stats/reports toggle
  - Catálogos API (/api/catalogos/* incluyendo ciudades y parroquias)
