# models.py
from pydantic import BaseModel
from typing import Optional, List
import datetime

# Clase base para no repetir campos
class UsuarioBase(BaseModel):
    email: str
    nombre: str
    apellido: str

# Clase que hereda de UsuarioBase para un usuario completo
class Usuario(UsuarioBase):
    id_usuario: int
    rol: str

    class Config:
        from_attributes = True

# Herencia y Polimorfismo: Aunque en Pydantic no es como en la lógica de negocio,
# el concepto de extender una clase base se mantiene.

# Clase para los datos de un pedido
class Pedido(BaseModel):
    id_pedido: int
    fecha_pedido: datetime.date
    monto_total: float
    estado: str
    cliente: Optional[str] = None
    vendedor: Optional[str] = None

    class Config:
        from_attributes = True

# Clase para recibir los datos del login
class LoginData(BaseModel):
    email: str
    contrasena: str