# Welcome Page Design — SEDER

## Summary
Rediseñar el dashboard actual (`/dashboard`) como una página de bienvenida con menú lateral, módulos agrupados por funcionalidad, imagen decorativa, y secciones de estadísticas/reportes ocultas hasta que el usuario las solicite.

## Layout

```
┌────────────────────────────────────────────────┐
│  SIDEBAR            │  MAIN CONTENT            │
│  ┌──────────┐       │  ┌────────────────────┐  │
│  │ Logo     │       │  │ Welcome + Image    │  │
│  │ SEDER    │       │  │ ┌──────┐ ┌───────┐ │  │
│  ├──────────┤       │  │ │Saludo│ │ ⛪    │ │  │
│  │ Admin    │       │  │ │      │ │Iglesia│ │  │
│  │ Adminis. │       │  │ └──────┘ └───────┘ │  │
│  ├──────────┤       │  │ [📊Stats][📄Rpts]  │  │
│  │ PERSONAS │       │  ├────────────────────┤  │
│  │ 👤 Miembros│     │  │ Stats Section (hidden)│  │
│  │ 👪 Familias│     │  │ ┌───┐ ┌───┐ ┌───┐  │  │
│  │ 💼 Profes.│      │  │ │ 5 │ │ 3 │ │ 1 │  │  │
│  │ 🎖️ Roles │      │  │ └───┘ └───┘ └───┘  │  │
│  │ 🤝 Grupos │      │  │ ┌─Gráfico──┐           │  │
│  ├──────────┤       │  │ └──────────┘           │  │
│  │ REGISTRO │       │  ├────────────────────┤  │
│  │ ✅ Asist. │      │  │ Reports Section (hidden)│  │
│  │ 📦 Invent│      │  │ 📥 Excel  📥 PDF    │  │
│  ├──────────┤       │  ├────────────────────┤  │
│  │ ADMINIS. │       │  │ Módulos disponibles │  │
│  │ 🔐 Usrs  │      │  │ ┌──┐ ┌──┐ ┌──┐      │  │
│  │ 🔧 Roles │      │  │ 👤│ 👪│ 💼│      │  │
│  │ ⛪ Igles. │      │  │ └──┘ └──┘ └──┘      │  │
│  │ 📋 Audit.│      │  │ ┌──┐ ┌──┐ ┌──┐      │  │
│  │ 📄 CSV   │      │  │ 🎖│ 🤝│ ✅│      │  │
│  ├──────────┤       │  │ └──┘ └──┘ └──┘      │  │
│  │🚪 Cerrar │       │  └────────────────────┘  │
│  │  Sesión  │       │                          │
│  └──────────┘       │                          │
└────────────────────────────────────────────────┘
```

## Components

### 1. Sidebar (left, ~220px, dark indigo `#1E1B4B`)
- **Logo area**: Cuadro blanco con "S", texto "SEDER"
- **User info**: Nombre y rol del usuario conectado
- **Navigation groups** with section headers:
  - **PERSONAS**: Miembros, Familias, Profesiones, Roles Eclesiásticos, Grupos
  - **REGISTRO**: Asistencia, Inventario
  - **ADMINISTRACIÓN**: Usuarios, Roles, Iglesias, Auditoría, Carga CSV
- **Logout**: Al final del sidebar, en rojo suave
- Solo se muestran items para los que el usuario tiene permiso

### 2. Main Content (flex-1, light gray `#F9FAFB`)
- **Welcome row**: Título + subtítulo + botones toggle (Stats, Reports) + imagen decorativa (derecha)
- **Stats section** (hidden by default, toggle con botón "📊 Estadísticas"):
  - 6 tarjetas numéricas (Miembros, Familias, Iglesias, Grupos, Artículos, Asistencias)
  - 3 gráficos Chart.js (Sexo, Estado, Inventario)
- **Reports section** (hidden by default, toggle con botón "📄 Reportes"):
  - 4 enlaces de descarga (Miembros Excel/PDF, Inventario Excel/PDF)
- **Modules grid**: Tarjetas de acceso rápido a cada módulo (ícono + nombre)

### 3. Image
- Lado derecho del saludo de bienvenida
- Ilustración decorativa (SVG inline con ícono de iglesia/cruz)
- Fondo gradiente suave (indigo claro)

## Behavior

### Toggle Stats/Reports
- Cada botón es un toggle independiente
- Click "📊 Estadísticas": muestra/oculta la sección de stats + gráficos
- Click "📄 Reportes": muestra/oculta la sección de reportes
- Transición suave (clases Tailwind `hidden`/`block`)

### Navigation
- Click en sidebar item o card → `window.location.href = '/modulo'`
- Item activo en sidebar se resalta (fondo semitransparente)
- Mantener el token JWT en localStorage para todas las peticiones

### Permission filtering
- Al cargar la página, fetch a `/api/auth/permisos`
- Iterar los módulos y mostrar solo aquellos cuyo permiso existe
- Si no tiene ningún permiso de un grupo completo, ocultar ese grupo

## Data Flow
1. Page load → check token → if missing, redirect to `/`
2. Fetch `/api/auth/permisos` → determine qué módulos mostrar
3. Fetch `/api/dashboard/stats` → preparar datos para cuando se activen stats
4. Render modules grid y sidebar según permisos
5. Estadísticas y reportes se renderizan al hacer clic en toggle (lazy)

## Tech Stack
- Tailwind CSS via CDN
- Chart.js via CDN (solo cuando se activan stats)
- Vanilla JS
- Backend: rutas existentes sin cambios

## Files to modify
- `backend/app/templates/dashboard.html` — reemplazar completamente
- `backend/app/templates/login.html` — cambiar redirect de `/dashboard` a `/dashboard` (ya apunta ahí)
- `backend/app/main.py` — posiblemente ajustar ruta /dashboard si es necesario

## Backend
No se requieren cambios en el backend. Todas las rutas API (`/api/auth/permisos`, `/api/dashboard/stats`, etc.) ya existen.
