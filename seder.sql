-- ============================================================================
-- SCRIPT DE BASE DE DATOS PARA GESTIÓN ECLESIAL E INVENTARIO
-- ============================================================================

SET NAMES utf8mb4;

-- ----------------------------------------------------------------------------
-- 1. TABLAS CATÁLOGO DE UBICACIÓN GEOGRÁFICA
-- ----------------------------------------------------------------------------

CREATE TABLE Paises (
    ID_Pais INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Pais VARCHAR(100) NOT NULL
);

CREATE TABLE Estados (
    ID_Estado INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Estado VARCHAR(100) NOT NULL,
    ID_Pais INT NOT NULL,
    FOREIGN KEY (ID_Pais) REFERENCES Paises(ID_Pais)
);

CREATE TABLE Municipios (
    ID_Municipio INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Municipio VARCHAR(100) NOT NULL,
    ID_Estado INT NOT NULL,
    FOREIGN KEY (ID_Estado) REFERENCES Estados(ID_Estado)
);

CREATE TABLE Parroquias (
    ID_Parroquia INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Parroquia VARCHAR(100) NOT NULL,
    ID_Municipio INT NOT NULL,
    FOREIGN KEY (ID_Municipio) REFERENCES Municipios(ID_Municipio)
);

CREATE TABLE Ciudades (
    ID_Ciudad INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Ciudad VARCHAR(100) NOT NULL,
    ID_Estado INT NOT NULL,
    FOREIGN KEY (ID_Estado) REFERENCES Estados(ID_Estado)
);

-- ----------------------------------------------------------------------------
-- 2. TABLAS CATÁLOGO DE REFERENCIA
-- ----------------------------------------------------------------------------

CREATE TABLE Profesiones (
    ID_Profesion INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Profesion VARCHAR(100) NOT NULL
);

CREATE TABLE Oficios (
    ID_Oficio INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Oficio VARCHAR(100) NOT NULL
);

CREATE TABLE Roles (
    ID_Rol INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Rol VARCHAR(100) NOT NULL,
    Descripcion TEXT
);

CREATE TABLE Categorias_Inventario (
    ID_Categoria INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Categoria VARCHAR(100) NOT NULL
);

CREATE TABLE Permisos (
    ID_Permiso INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Permiso VARCHAR(50) NOT NULL UNIQUE,
    Descripcion TEXT
);

CREATE TABLE Roles_Permisos (
    ID_Rol INT NOT NULL,
    ID_Permiso INT NOT NULL,
    PRIMARY KEY (ID_Rol, ID_Permiso),
    FOREIGN KEY (ID_Rol) REFERENCES Roles(ID_Rol) ON DELETE CASCADE,
    FOREIGN KEY (ID_Permiso) REFERENCES Permisos(ID_Permiso) ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 3. ESTRUCTURA DE IGLESIAS
-- ----------------------------------------------------------------------------

CREATE TABLE Iglesias (
    ID_Iglesia INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Iglesia VARCHAR(150) NOT NULL,
    ID_Iglesia_Madre INT NULL,
    Direccion TEXT NOT NULL,
    Telefono_Iglesia_movil VARCHAR(20),
    Telefono_fijo VARCHAR(20),
    Correo VARCHAR(100),
    ID_Ciudad INT NOT NULL,
    ID_Parroquia INT NOT NULL,
    Creado_En DATETIME DEFAULT CURRENT_TIMESTAMP,
    Actualizado_En DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Iglesia_Madre) REFERENCES Iglesias(ID_Iglesia),
    FOREIGN KEY (ID_Ciudad) REFERENCES Ciudades(ID_Ciudad),
    FOREIGN KEY (ID_Parroquia) REFERENCES Parroquias(ID_Parroquia)
);

-- ----------------------------------------------------------------------------
-- 4. ESTRUCTURA DE NÚCLEO FAMILIAR
-- ----------------------------------------------------------------------------

CREATE TABLE Familias (
    ID_Familia INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Familia VARCHAR(150) NOT NULL,
    ID_Cabeza_Familia INT NULL,
    Creado_En DATETIME DEFAULT CURRENT_TIMESTAMP,
    Actualizado_En DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 5. TABLA PRINCIPAL: MIEMBROS
-- ----------------------------------------------------------------------------

CREATE TABLE Miembros (
    ID_Miembro INT AUTO_INCREMENT PRIMARY KEY,
    ID_Iglesia INT NOT NULL,
    Cedula VARCHAR(20) UNIQUE NOT NULL,
    Nombres VARCHAR(100) NOT NULL,
    Apellidos VARCHAR(100) NOT NULL,
    Fecha_Nacimiento DATE,
    Telefono VARCHAR(20),
    Correo_Electronico VARCHAR(100),
    Fecha_Bautismo DATE,
    Fecha_Conversion DATE,
    Estado ENUM('Activo', 'Inactivo', 'Visitante', 'Trasladado', 'Excomulgado') DEFAULT 'Visitante',
    ID_Familia INT NULL,
    ID_Ciudad INT NOT NULL,
    ID_Parroquia INT NOT NULL,
    Direccion TEXT,
    Sexo CHAR(1) CHECK (Sexo IN ('M', 'F')),
    Estado_Civil VARCHAR(50),
    Creado_En DATETIME DEFAULT CURRENT_TIMESTAMP,
    Actualizado_En DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Iglesia) REFERENCES Iglesias(ID_Iglesia),
    FOREIGN KEY (ID_Familia) REFERENCES Familias(ID_Familia),
    FOREIGN KEY (ID_Ciudad) REFERENCES Ciudades(ID_Ciudad),
    FOREIGN KEY (ID_Parroquia) REFERENCES Parroquias(ID_Parroquia)
);

ALTER TABLE Familias
ADD CONSTRAINT FK_Cabeza_Familia
FOREIGN KEY (ID_Cabeza_Familia) REFERENCES Miembros(ID_Miembro);

-- ----------------------------------------------------------------------------
-- 6. TABLAS INTERMEDIAS Y DE RELACIÓN (MIEMBROS)
-- ----------------------------------------------------------------------------

CREATE TABLE Miembros_Profesiones (
    ID_Miembro INT NOT NULL,
    ID_Profesion INT NOT NULL,
    PRIMARY KEY (ID_Miembro, ID_Profesion),
    FOREIGN KEY (ID_Miembro) REFERENCES Miembros(ID_Miembro) ON DELETE CASCADE,
    FOREIGN KEY (ID_Profesion) REFERENCES Profesiones(ID_Profesion) ON DELETE CASCADE
);

CREATE TABLE Miembros_Oficios (
    ID_Miembro INT NOT NULL,
    ID_Oficio INT NOT NULL,
    PRIMARY KEY (ID_Miembro, ID_Oficio),
    FOREIGN KEY (ID_Miembro) REFERENCES Miembros(ID_Miembro) ON DELETE CASCADE,
    FOREIGN KEY (ID_Oficio) REFERENCES Oficios(ID_Oficio) ON DELETE CASCADE
);

CREATE TABLE Miembros_Roles (
    ID_Miembro INT NOT NULL,
    ID_Rol INT NOT NULL,
    Fecha_Asignacion DATE,
    Estado_Rol ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    PRIMARY KEY (ID_Miembro, ID_Rol),
    FOREIGN KEY (ID_Miembro) REFERENCES Miembros(ID_Miembro) ON DELETE CASCADE,
    FOREIGN KEY (ID_Rol) REFERENCES Roles(ID_Rol) ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 7. USUARIOS DEL SISTEMA (LOGIN, AUTENTICACIÓN)
-- ----------------------------------------------------------------------------

CREATE TABLE Usuarios (
    ID_Usuario INT AUTO_INCREMENT PRIMARY KEY,
    ID_Miembro INT NULL,
    Nombre_Usuario VARCHAR(50) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password_Hash VARCHAR(255) NOT NULL,
    ID_Rol INT NOT NULL,
    Activo BOOLEAN DEFAULT TRUE,
    Ultimo_Acceso DATETIME NULL,
    Creado_En DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Miembro) REFERENCES Miembros(ID_Miembro) ON DELETE SET NULL,
    FOREIGN KEY (ID_Rol) REFERENCES Roles(ID_Rol)
);

-- ----------------------------------------------------------------------------
-- 8. MINISTERIOS, ASISTENCIA Y OPERACIONES DOMINICALES
-- ----------------------------------------------------------------------------

CREATE TABLE Ministerios_Grupos (
    ID_Grupo INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Grupo VARCHAR(150) NOT NULL,
    Descripcion TEXT,
    ID_Lider INT NULL,
    FOREIGN KEY (ID_Lider) REFERENCES Miembros(ID_Miembro) ON DELETE SET NULL
);

CREATE TABLE Miembros_Grupos (
    ID_Miembro INT NOT NULL,
    ID_Grupo INT NOT NULL,
    Rol VARCHAR(100) DEFAULT 'Integrante',
    PRIMARY KEY (ID_Miembro, ID_Grupo),
    FOREIGN KEY (ID_Miembro) REFERENCES Miembros(ID_Miembro) ON DELETE CASCADE,
    FOREIGN KEY (ID_Grupo) REFERENCES Ministerios_Grupos(ID_Grupo) ON DELETE CASCADE
);

CREATE TABLE Registro_Asistencia (
    ID_Asistencia INT AUTO_INCREMENT PRIMARY KEY,
    ID_Miembro INT NOT NULL,
    Fecha DATE NOT NULL,
    Tipo_Evento VARCHAR(100) NOT NULL,
    Estado_Asistencia ENUM('Presente', 'Ausente', 'Justificado') NOT NULL,
    Creado_En DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Miembro) REFERENCES Miembros(ID_Miembro) ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 9. AUDITORÍA (LOG DE ACTIVIDADES DEL SISTEMA)
-- ----------------------------------------------------------------------------

CREATE TABLE Auditoria (
    ID_Auditoria INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,
    Accion VARCHAR(50) NOT NULL,
    Tabla_Afectada VARCHAR(50),
    ID_Registro_Afectado INT,
    Detalle TEXT,
    Direccion_IP VARCHAR(45),
    Fecha_Hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario) ON DELETE SET NULL
);

-- ----------------------------------------------------------------------------
-- 10. GESTIÓN DE INVENTARIO Y RESGUARDOS
-- ----------------------------------------------------------------------------

CREATE TABLE Inventario (
    ID_Articulo INT AUTO_INCREMENT PRIMARY KEY,
    ID_Iglesia INT NOT NULL,
    ID_Categoria INT NOT NULL,
    Nombre_Articulo VARCHAR(150) NOT NULL,
    Descripcion TEXT,
    Marca VARCHAR(100),
    Modelo VARCHAR(100),
    Numero_Serie VARCHAR(100),
    Cantidad INT NOT NULL DEFAULT 1,
    Estado_Articulo ENUM('Excelente', 'Bueno', 'Requiere Mantenimiento', 'Dañado') DEFAULT 'Bueno',
    Ubicacion_Interna VARCHAR(150),
    ID_Miembro_Resguarda INT NULL,
    Tipo_Ubicacion ENUM('En el Templo', 'En Resguardo Externo (Casa del miembro)', 'En Tránsito') DEFAULT 'En el Templo',
    Ubicacion_Detallada TEXT,
    Creado_En DATETIME DEFAULT CURRENT_TIMESTAMP,
    Actualizado_En DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Iglesia) REFERENCES Iglesias(ID_Iglesia),
    FOREIGN KEY (ID_Categoria) REFERENCES Categorias_Inventario(ID_Categoria),
    FOREIGN KEY (ID_Miembro_Resguarda) REFERENCES Miembros(ID_Miembro) ON DELETE SET NULL
);

CREATE TABLE Historial_Resguardos (
    ID_Resguardo INT AUTO_INCREMENT PRIMARY KEY,
    ID_Articulo INT NOT NULL,
    ID_Miembro_Responsable INT NOT NULL,
    Fecha_Salida_Asignacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Fecha_Devolucion_Prevista DATE NULL,
    Fecha_Devolucion_Real DATETIME NULL,
    Estado_Entrega VARCHAR(100) NOT NULL,
    Estado_Devolucion VARCHAR(100) NULL,
    Notas_Observaciones TEXT,
    Creado_En DATETIME DEFAULT CURRENT_TIMESTAMP,
    Actualizado_En DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Articulo) REFERENCES Inventario(ID_Articulo) ON DELETE CASCADE,
    FOREIGN KEY (ID_Miembro_Responsable) REFERENCES Miembros(ID_Miembro)
);

-- ----------------------------------------------------------------------------
-- 11. ÍNDICES
-- ----------------------------------------------------------------------------

CREATE INDEX idx_miembros_nombre ON Miembros(Nombres, Apellidos);
CREATE INDEX idx_miembros_iglesia ON Miembros(ID_Iglesia);
CREATE INDEX idx_miembros_estado ON Miembros(Estado);
CREATE INDEX idx_inventario_categoria ON Inventario(ID_Categoria);
CREATE INDEX idx_inventario_iglesia ON Inventario(ID_Iglesia);
CREATE INDEX idx_inventario_estado ON Inventario(Estado_Articulo);
CREATE INDEX idx_asistencia_fecha ON Registro_Asistencia(Fecha);
CREATE INDEX idx_asistencia_miembro ON Registro_Asistencia(ID_Miembro);
CREATE INDEX idx_familias_cabeza ON Familias(ID_Cabeza_Familia);
CREATE INDEX idx_auditoria_usuario ON Auditoria(ID_Usuario);
CREATE INDEX idx_auditoria_fecha ON Auditoria(Fecha_Hora);
CREATE INDEX idx_usuarios_rol ON Usuarios(ID_Rol);
CREATE INDEX idx_historial_articulo ON Historial_Resguardos(ID_Articulo);

-- ----------------------------------------------------------------------------
-- 12. DATOS SEMILLA
-- ----------------------------------------------------------------------------

INSERT INTO Roles (Nombre_Rol, Descripcion) VALUES
('Administrador', 'Acceso total a todas las funcionalidades del sistema'),
('Secretario', 'Gestión de miembros, inventario y reportes'),
('Consulta', 'Solo visualización de datos y reportes');

INSERT INTO Permisos (Nombre_Permiso, Descripcion) VALUES
('miembros.ver', 'Ver listado y detalle de miembros'),
('miembros.crear', 'Registrar nuevos miembros'),
('miembros.editar', 'Editar información de miembros'),
('miembros.eliminar', 'Eliminar miembros del sistema'),
('inventario.ver', 'Ver listado y detalle del inventario'),
('inventario.crear', 'Registrar nuevos artículos'),
('inventario.editar', 'Editar información de artículos'),
('inventario.eliminar', 'Eliminar artículos del inventario'),
('reportes.ver', 'Ver y exportar reportes'),
('reportes.exportar', 'Exportar reportes en Excel y PDF'),
('dashboard.ver', 'Ver dashboard estadístico'),
('usuarios.gestionar', 'Gestionar usuarios del sistema'),
('roles.gestionar', 'Gestionar roles y permisos'),
('csv.importar', 'Importar datos masivos desde CSV'),
('auditoria.ver', 'Ver registros de auditoría'),
('familias.ver', 'Ver núcleos familiares'),
('familias.crear', 'Registrar nuevas familias'),
('familias.editar', 'Editar información de familias'),
('familias.eliminar', 'Eliminar familias'),
('asistencia.ver', 'Ver registros de asistencia'),
('asistencia.crear', 'Registrar asistencia'),
('asistencia.editar', 'Editar registros de asistencia'),
('asistencia.eliminar', 'Eliminar registros de asistencia'),
('categorias.ver', 'Ver categorías de inventario'),
('categorias.crear', 'Crear categorías de inventario'),
('categorias.editar', 'Editar categorías de inventario'),
('categorias.eliminar', 'Eliminar categorías de inventario'),
('iglesias.ver', 'Ver listado y detalle de iglesias'),
('iglesias.crear', 'Registrar nuevas iglesias'),
('iglesias.editar', 'Editar información de iglesias'),
('iglesias.eliminar', 'Eliminar iglesias'),
('geografia.ver', 'Ver países, estados, municipios, ciudades y parroquias'),
('geografia.crear', 'Crear registros geográficos'),
('geografia.editar', 'Editar registros geográficos'),
('geografia.eliminar', 'Eliminar registros geográficos');

INSERT INTO Roles_Permisos (ID_Rol, ID_Permiso)
SELECT 1, ID_Permiso FROM Permisos;

INSERT INTO Roles_Permisos (ID_Rol, ID_Permiso)
SELECT 2, ID_Permiso FROM Permisos
WHERE Nombre_Permiso NOT IN ('usuarios.gestionar', 'roles.gestionar', 'auditoria.ver');

INSERT INTO Roles_Permisos (ID_Rol, ID_Permiso)
SELECT 3, ID_Permiso FROM Permisos
WHERE Nombre_Permiso IN ('miembros.ver', 'inventario.ver', 'reportes.ver', 'dashboard.ver', 'familias.ver', 'asistencia.ver');
