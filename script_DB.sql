-- Crear la base de datos
CREATE DATABASE PandaTaT;

-- Usar la base de datos recién creada
USE PandaTaT;

-- Tabla para los roles de usuario
CREATE TABLE Roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla para los estados de los pedidos
CREATE TABLE Estado_pedidos (
    id_estado INT PRIMARY KEY AUTO_INCREMENT,
    nombre_estado VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla para los usuarios
CREATE TABLE Usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES Roles(id_rol)
);

-- Tabla para los pedidos
CREATE TABLE Pedidos (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    fecha_pedido DATE NOT NULL,
    monto_total DECIMAL(10,2) NOT NULL,
    id_usuario_cliente INT NOT NULL,
    id_estado INT NOT NULL,
    id_usuario_vendedor INT, -- Opcional, si se desea registrar el vendedor
    FOREIGN KEY (id_usuario_cliente) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_estado) REFERENCES Estado_pedidos(id_estado),
    FOREIGN KEY (id_usuario_vendedor) REFERENCES Usuarios(id_usuario)
);

INSERT INTO Roles (nombre_rol) VALUES
('Administrador'),
('Gerente de zona'),
('Vendedor'),
('Cliente');

-- Inserción de datos iniciales para Estado_pedidos
INSERT INTO Estado_pedidos (nombre_estado) VALUES
('Enviado'),
('Cancelado'),
('Pagado'),
('Reenviado');

-- Inserción de un usuario por cada rol
INSERT INTO Usuarios (nombre, apellido, email, contrasena, id_rol) VALUES
('Ana', 'García', 'ana.admin@example.com', 'ana123', (SELECT id_rol FROM Roles WHERE nombre_rol = 'Administrador')),
('Carlos', 'Díaz', 'carlos.gerente@example.com', 'carlos123', (SELECT id_rol FROM Roles WHERE nombre_rol = 'Gerente de zona')),
('Laura', 'Pérez', 'laura.vendedor@example.com', 'laura123', (SELECT id_rol FROM Roles WHERE nombre_rol = 'Vendedor')),
('Juan', 'Martínez', 'juan.cliente@example.com', 'juan123', (SELECT id_rol FROM Roles WHERE nombre_rol = 'Cliente'));


INSERT INTO Pedidos (fecha_pedido, monto_total, id_usuario_cliente, id_estado, id_usuario_vendedor) VALUES
('2025-05-20', 150000, (SELECT id_usuario FROM Usuarios WHERE email = 'juan.cliente@example.com'), (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Enviado'), (SELECT id_usuario FROM Usuarios WHERE email = 'laura.vendedor@example.com')),
('2025-05-22', 300000, (SELECT id_usuario FROM Usuarios WHERE email = 'juan.cliente@example.com'), (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Pagado'), (SELECT id_usuario FROM Usuarios WHERE email = 'laura.vendedor@example.com')),
('2025-05-25', 75000, (SELECT id_usuario FROM Usuarios WHERE email = 'juan.cliente@example.com'), (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Cancelado'), NULL), -- Pedido cancelado, sin vendedor asignado inicialmente
('2025-05-28', 220000, (SELECT id_usuario FROM Usuarios WHERE email = 'juan.cliente@example.com'), (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Reenviado'), (SELECT id_usuario FROM Usuarios WHERE email = 'laura.vendedor@example.com')),
('2025-06-01', 99000, (SELECT id_usuario FROM Usuarios WHERE email = 'juan.cliente@example.com'), (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Pagado'), (SELECT id_usuario FROM Usuarios WHERE email = 'laura.vendedor@example.com'));