# main.py
# API RESTful para ser consumida por un frontend.

from fastapi import FastAPI, HTTPException
from typing import List
from database import cleverCursor
from models import Usuario, Pedido, LoginData # Importamos los modelos Pydantic

app = FastAPI(
    title="PandaTaT API",
    description="API para la gestión de usuarios y pedidos del sistema PandaTaT.",
    version="1.0.0"
)

# --- Funciones Auxiliares para Mapeo de Datos ---
# Estas funciones convierten los resultados de la base de datos (tuplas) a diccionarios
# para que FastAPI pueda convertirlos a JSON usando los modelos Pydantic.

def map_to_pedido(record):
    if not record:
        return None
    return {
        "id_pedido": record[0],
        "fecha_pedido": record[1],
        "monto_total": record[2],
        "estado": record[3],
        "cliente": record[4],
        "vendedor": record[5] if record[5] else "N/A"
    }

#---------------------------------------------------------------------------
# ENDPOINT DE AUTENTICACIÓN
#---------------------------------------------------------------------------

@app.post("/login", response_model=Usuario, tags=["Autenticación"])
def login(login_data: LoginData):
    """
    Verifica las credenciales de un usuario y, si son correctas,
    devuelve los datos del usuario en formato JSON.
    """
    query = """
        SELECT u.id_usuario, u.nombre, u.apellido, u.email, r.nombre_rol
        FROM Usuarios u
        JOIN Roles r ON u.id_rol = r.id_rol
        WHERE u.email = %s AND u.contrasena = %s
    """
    cleverCursor.execute(query, (login_data.email, login_data.contrasena))
    user_record = cleverCursor.fetchone()

    if not user_record:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    return {
        "id_usuario": user_record[0],
        "nombre": user_record[1],
        "apellido": user_record[2],
        "email": user_record[3],
        "rol": user_record[4]
    }

#---------------------------------------------------------------------------
# ENDPOINTS DE PEDIDOS
#---------------------------------------------------------------------------

@app.get("/pedidos", response_model=List[Pedido], tags=["Pedidos"])
def get_todos_los_pedidos():
    """
    Devuelve una lista de todos los pedidos en el sistema.
    Ideal para un dashboard de administrador.
    """
    query = """
        SELECT p.id_pedido, p.fecha_pedido, p.monto_total, e.nombre_estado,
               CONCAT(c.nombre, ' ', c.apellido) AS cliente,
               CONCAT(v.nombre, ' ', v.apellido) AS vendedor
        FROM Pedidos p
        JOIN Estado_pedidos e ON p.id_estado = e.id_estado
        JOIN Usuarios c ON p.id_usuario_cliente = c.id_usuario
        LEFT JOIN Usuarios v ON p.id_usuario_vendedor = v.id_usuario
        ORDER BY p.id_pedido
    """
    cleverCursor.execute(query)
    pedidos_records = cleverCursor.fetchall()
    
    # Mapeamos cada registro a un diccionario antes de devolverlo
    return [map_to_pedido(p) for p in pedidos_records]

@app.get("/usuarios/{usuario_id}/pedidos", response_model=List[Pedido], tags=["Pedidos"])
def get_pedidos_por_usuario(usuario_id: int):
    """
    Devuelve el historial de pedidos de un usuario específico (cliente).
    Un frontend llamaría a este endpoint después de que un cliente inicie sesión.
    """
    # Primero verificamos si el usuario existe para dar un mejor feedback
    cleverCursor.execute("SELECT id_usuario FROM Usuarios WHERE id_usuario = %s", (usuario_id,))
    if not cleverCursor.fetchone():
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    query = """
        SELECT p.id_pedido, p.fecha_pedido, p.monto_total, e.nombre_estado,
               CONCAT(c.nombre, ' ', c.apellido) AS cliente,
               CONCAT(v.nombre, ' ', v.apellido) AS vendedor
        FROM Pedidos p
        JOIN Estado_pedidos e ON p.id_estado = e.id_estado
        JOIN Usuarios c ON p.id_usuario_cliente = c.id_usuario
        LEFT JOIN Usuarios v ON p.id_usuario_vendedor = v.id_usuario
        WHERE p.id_usuario_cliente = %s
        ORDER BY p.fecha_pedido DESC
    """
    cleverCursor.execute(query, (usuario_id,))
    pedidos_records = cleverCursor.fetchall()
    
    return [map_to_pedido(p) for p in pedidos_records]

#---------------------------------------------------------------------------
# ENDPOINTS DE USUARIOS
#---------------------------------------------------------------------------

@app.get("/usuarios", response_model=List[Usuario], tags=["Usuarios"])
def get_usuarios_por_rol(rol: str):
    """
    Devuelve una lista de usuarios filtrados por rol.
    Ejemplo de uso en frontend: /usuarios?rol=Vendedor
    """
    # Validamos que el rol exista para evitar inyección SQL o errores
    cleverCursor.execute("SELECT nombre_rol FROM Roles WHERE nombre_rol = %s", (rol,))
    if not cleverCursor.fetchone():
        raise HTTPException(status_code=400, detail=f"El rol '{rol}' no es válido.")

    query = """
        SELECT u.id_usuario, u.nombre, u.apellido, u.email, r.nombre_rol
        FROM Usuarios u
        JOIN Roles r ON u.id_rol = r.id_rol
        WHERE r.nombre_rol = %s
    """
    cleverCursor.execute(query, (rol,))
    user_records = cleverCursor.fetchall()

    if not user_records:
        raise HTTPException(status_code=404, detail=f"No se encontraron usuarios con el rol '{rol}'")

    # Mapeamos cada registro a la estructura del modelo Pydantic
    return [
        {
            "id_usuario": u[0], "nombre": u[1], "apellido": u[2], 
            "email": u[3], "rol": u[4]
        } for u in user_records
    ]