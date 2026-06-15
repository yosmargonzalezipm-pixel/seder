# SEDER - Sistema de Registro Eclesiástico

Sistema de administración eclesial para la Iglesia Dios es Amor, Tipuro.

## Arquitectura

| Servicio | Tecnología | Puerto Host |
|---|---|---|
| **Backend** | FastAPI (Python 3.12) | `8086` |
| **Base de Datos** | MySQL 8.0 | `3307` |
| **phpMyAdmin** | phpMyAdmin 5.2 | `8085` |

## Acceso

| Aplicación | URL | Usuario | Contraseña |
|---|---|---|---|
| **Sistema SEDER** | http://localhost:8086 | `admin` | `admin123` |
| **phpMyAdmin** | http://localhost:8085 | `seder_user` | `seder_pass` |
| **Usuario consulta** | http://localhost:8086 | `test` | `test123` |

## Roles del Sistema

| Rol | Descripción |
|---|---|
| **Administrador** | Acceso completo a todos los módulos y CRUDs |
| **Secretario** | Permisos limitados según configuración |
| **Consulta** | Solo lectura |

## Módulos Implementados

- **Miembros** — CRUD completo con todos los campos del formulario, incluyendo Profesiones/Oficios multi-select y fechas espirituales
- **Familias** — Gestión de núcleos familiares
- **Asistencia** — Registro y control de asistencia a eventos
- **Inventario** — Control de bienes y activos de la iglesia
- **Resguardos** — Historial de asignación y devolución de artículos
- **Ministerios** — Gestión de ministerios con miembros y roles (Integrante, Vocal, Secretario, Tesorero, Director, Asistente)
- **Roles Eclesiásticos** — Roles dentro de la iglesia y asignación a miembros
- **Profesiones y Oficios** — Catálogos para perfiles de miembros
- **Iglesias** — Gestión de sedes o templos
- **Usuarios y Roles** — Administración de usuarios del sistema y permisos
- **Auditoría** — Registro de cambios y actividades
- **Dashboard** — Panel principal con estadísticas, gráficos y acceso rápido a módulos
- **Carga Masiva CSV** — Importación de miembros e inventario desde archivos CSV
- **Reportes** — Exportación a Excel y PDF con vista previa en pantalla

## Comandos

### Iniciar contenedores
```bash
docker-compose up -d
```

### Detener contenedores
```bash
docker-compose down
```

### Ver logs
```bash
docker-compose logs -f backend
docker-compose logs -f mysql
docker-compose logs -f phpmyadmin
```

### Reiniciar backend (refleja cambios de código)
```bash
docker-compose restart backend
```

### Reconstruir backend (tras cambios en requirements.txt o Dockerfile)
```bash
docker-compose build backend
docker-compose restart backend
```

### Actualizar desde Git y aplicar cambios
```bash
git pull
docker-compose down
docker-compose up -d
```

### Acceder a MySQL directamente
```bash
docker-compose exec mysql mysql -useder_user -pseder_pass seder
```

## Estructura del Proyecto

```
seder/
├── backend/
│   ├── app/
│   │   ├── main.py              # Punto de entrada FastAPI
│   │   ├── config.py            # Configuración de la aplicación
│   │   ├── database.py          # Conexión a la base de datos
│   │   ├── models/              # Modelos SQLAlchemy
│   │   ├── schemas/             # Schemas Pydantic
│   │   ├── routers/             # Endpoints de la API
│   │   ├── templates/           # Plantillas HTML (Jinja2)
│   │   ├── static/              # Archivos estáticos
│   │   ├── utils/               # Utilidades (seguridad, etc.)
│   │   └── reportes/            # Generación de Excel y PDF
│   ├── Dockerfile
│   └── requirements.txt
├── db/
│   └── init.sql                 # Script de inicialización de la BD
├── docker-compose.yml
├── seder.sql                    # Schema completo de la base de datos
└── .env                         # Variables de entorno (MySQL)
```

## Tecnologías

- **Backend:** FastAPI, SQLAlchemy, JWT (python-jose), bcrypt (passlib)
- **Base de Datos:** MySQL 8.0
- **Reportes:** openpyxl (Excel), reportlab (PDF)
- **Frontend:** Tailwind CSS vía CDN, JavaScript vanilla, Chart.js
- **Infraestructura:** Docker, Docker Compose v1.29.2
