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
- Charset: MySQL servidor en `utf8mb4` vía `command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci`
- Seed files inician con `SET NAMES utf8mb4` para evitar doble-codificación
- Backend conecta con `charset=utf8mb4` en connection string

## Decisiones Clave
- `Miembro` en `miembro.py` (no en `usuario.py`) para evitar duplicación de tabla SQLAlchemy
- phpMyAdmin usa `phpmyadmin:5.2` (imagen más pequeña, evita `latest`)
- bcrypt 4.1.3 pinneado para compatibilidad con passlib
- `/grupos` redirige a `/ministerios` con 307 (permisos renombrados de `grupos.*` a `ministerios.*`)
- Logo físico (`logoDiosesamor.jpg`) en `/static/` pero no se usa; se muestra texto "Dios es Amor / 1 Juan 4:8"
- Charset: MySQL por defecto usa `latin1`. Se corrigió con 3 medidas: (1) `command` en docker-compose para server charset, (2) `SET NAMES utf8mb4` en seed files, (3) UPDATE directo a datos existentes con doble-codificación (`Ã³` → `ó`)
- Imagen backend: no usar `docker export/import` para imágenes docker-compose — elimina `ContainerConfig` y rompe `docker-compose up`. Usar `docker commit` o rebuild limpio en su lugar.
- Parentescos: catálogo fijo en tabla `Parentescos` con 12 valores predefinidos. `Miembros.ID_Parentesco` FK opcional. Gestionable desde modal en página de familias.

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
    - **Auditoría**: Logging automático de crear/actualizar/eliminar en todos los módulos. Utilidad en `backend/app/utils/auditoria.py`. Datos visibles en `/auditoria`.
  - **Familias + Parentesco**: Las familias muestran miembros con parentesco en la tabla. Modal "Gestionar Miembros" permite agregar/quitar miembros y asignar parentesco (catálogo fijo: Jefe de Hogar, Cónyuge, Hijo/a, etc). Endpoints: `POST/DELETE /api/familias/{id}/miembros/{miembro_id}`.

## Fixes Aplicados
- **UTF-8 / acentos**: Datos de Roles con doble-codificación corregidos via UPDATE. Causa raíz: MySQL con charset latin1 por defecto. Medidas: (1) `--character-set-server=utf8mb4` en docker-compose, (2) `SET NAMES utf8mb4` en seed files, (3) UPDATE a datos existentes con `CONVERT(CAST(CONVERT(columna USING latin1) AS BINARY) USING utf8mb4)`.
- **Backend image**: Imagen se corrompió al hacer `docker export/import` (falta `ContainerConfig`, rompe docker-compose). Fix: `docker rmi` + rebuild limpio con `docker-compose build`.
