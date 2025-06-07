# Importando FastAPI y el cursor de la base de datos
from fastapi import FastAPI
from database import cleverCursor

# app = FastAPI() para crear la instancia de FastAPI
app = FastAPI()

#---------------------------------------------------------------------------
@app.get("/Pedidos")
def get_pedidos():
    cleverCursor.execute("SELECT * FROM Pedidos")
    pedidos = cleverCursor.fetchall()
    return {"pedidos": pedidos}
#---------------------------------------------------------------------------
@app.get("/Pedidos Enviados")
def get_pedidos_enviados():
    cleverCursor.execute("SELECT * FROM Pedidos WHERE id_estado = (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Enviado')")
    pedidos_enviados = cleverCursor.fetchall()
    return {"pedidos_enviados": pedidos_enviados}
#---------------------------------------------------------------------------
@app.get("/Pedidos Pagados")
def get_pedidos_pagados():
    cleverCursor.execute("SELECT * FROM Pedidos WHERE id_estado = (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Pagado')")
    pedidos_pagados = cleverCursor.fetchall()
    return {"pedidos_pagados": pedidos_pagados}
#---------------------------------------------------------------------------
@app.get("/Pedidos Cancelados")
def get_pedidos_cancelados():
    cleverCursor.execute("SELECT * FROM Pedidos WHERE id_estado = (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Cancelado')")
    pedidos_cancelados = cleverCursor.fetchall()
    return {"pedidos_cancelados": pedidos_cancelados}
#---------------------------------------------------------------------------
@app.get("/Pedidos Reenviados")
def get_pedidos_reenviados():
    cleverCursor.execute("SELECT * FROM Pedidos WHERE id_estado = (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Reenviado')")
    pedidos_reenviados = cleverCursor.fetchall()
    return {"pedidos_reenviados": pedidos_reenviados}
#---------------------------------------------------------------------------
@app.get("/Pedidos Pagados por Vendedor")
def get_pedidos_pagados_por_vendedor():
    cleverCursor.execute("""
        SELECT p.*, u.nombre, u.apellido 
        FROM Pedidos p
        JOIN Usuarios u ON p.id_usuario_vendedor = u.id_usuario
        WHERE p.id_estado = (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Pagado')
    """)
    pedidos_pagados_vendedor = cleverCursor.fetchall()
    return {"pedidos_pagados_vendedor": pedidos_pagados_vendedor}
#---------------------------------------------------------------------------
@app.get("/Pedidos Enviados por Vendedor")
def get_pedidos_enviados_por_vendedor():
    cleverCursor.execute("""
        SELECT p.*, u.nombre, u.apellido 
        FROM Pedidos p
        JOIN Usuarios u ON p.id_usuario_vendedor = u.id_usuario
        WHERE p.id_estado = (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Enviado')
    """)
    pedidos_enviados_vendedor = cleverCursor.fetchall()
    return {"pedidos_enviados_vendedor": pedidos_enviados_vendedor}
#---------------------------------------------------------------------------
@app.get("/Pedidos Cancelados por Vendedor")
def get_pedidos_cancelados_por_vendedor():
    cleverCursor.execute("""
        SELECT p.*, u.nombre, u.apellido 
        FROM Pedidos p
        JOIN Usuarios u ON p.id_usuario_vendedor = u.id_usuario
        WHERE p.id_estado = (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Cancelado')
    """)
    pedidos_cancelados_vendedor = cleverCursor.fetchall()
    return {"pedidos_cancelados_vendedor": pedidos_cancelados_vendedor}
#---------------------------------------------------------------------------
@app.get("/Pedidos Reenviados por Vendedor")
def get_pedidos_reenviados_por_vendedor():
    cleverCursor.execute("""
        SELECT p.*, u.nombre, u.apellido 
        FROM Pedidos p
        JOIN Usuarios u ON p.id_usuario_vendedor = u.id_usuario
        WHERE p.id_estado = (SELECT id_estado FROM Estado_pedidos WHERE nombre_estado = 'Reenviado')
    """)
    pedidos_reenviados_vendedor = cleverCursor.fetchall()
    return {"pedidos_reenviados_vendedor": pedidos_reenviados_vendedor}
#---------------------------------------------------------------------------
@app.get("/Pedidos por Cliente")
def get_pedidos_por_cliente():
    cleverCursor.execute("""
        SELECT p.*, u.nombre, u.apellido 
        FROM Pedidos p
        JOIN Usuarios u ON p.id_usuario_cliente = u.id_usuario
    """)
    pedidos_por_cliente = cleverCursor.fetchall()
    return {"pedidos_por_cliente": pedidos_por_cliente}
#---------------------------------------------------------------------------
@app.get("/usuarios admin")
def get_admin_users():
    cleverCursor.execute("SELECT * FROM Usuarios WHERE id_rol = (SELECT id_rol FROM Roles WHERE nombre_rol = 'Administrador')")
    admin_users = cleverCursor.fetchall()
    return {"admin_users": admin_users}
#---------------------------------------------------------------------------
@app.get("/usuarios vendedor")
def get_vendedor_users():
    cleverCursor.execute("SELECT * FROM Usuarios WHERE id_rol = (SELECT id_rol FROM Roles WHERE nombre_rol = 'Vendedor')")
    vendedor_users = cleverCursor.fetchall()
    return {"vendedor_users": vendedor_users}
#---------------------------------------------------------------------------
@app.get("/cliente")
def get_cliente_users():
    cleverCursor.execute("SELECT * FROM Usuarios WHERE id_rol = (SELECT id_rol FROM Roles WHERE nombre_rol = 'Cliente')")
    cliente_users = cleverCursor.fetchall()
    return {"cliente_users": cliente_users}
#---------------------------------------------------------------------------
@app.get("/gerentes de zona")
def get_gerentes_de_zona():
    cleverCursor.execute("SELECT * FROM Usuarios WHERE id_rol = (SELECT id_rol FROM Roles WHERE nombre_rol = 'Gerente de Zona')")
    gerentes_de_zona = cleverCursor.fetchall()
    return {"gerentes_de_zona": gerentes_de_zona}
