from database import mysqlConn, cleverCursor
import datetime


# funcion para validar roles permitidos
def validar_rol(func):
    def wrapper(self):
        if self.rol not in ["aspirante", "consultor"]:
            print("Rol no válido. Solo se permite 'aspirante' o 'consultor'.")
            return
        return func(self)

    return wrapper


# ---------------------------------------------------------------------------------------------------------------------
# Clase usuario para crear usuarios y perfiles
class Usuario:
    def __init__(self, nombre, apellido, correo, contrasena, rol):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol

    @validar_rol  # Decorador para validar el rol
    def guardar_usuario(self):
        # Buscar ID del rol
        cleverCursor.execute("SELECT id FROM roles WHERE nombre = %s", (self.rol,))
        rol_result = cleverCursor.fetchone()
        if not rol_result:
            print("El rol no existe en la base de datos.")
            return
        rol_id = rol_result[0]

        # Insertar en la tabla usuarios
        cleverCursor.execute(
            "INSERT INTO usuarios (nombre_completo, email, contrasena, rol_id) VALUES (%s, %s, %s, %s)",
            (self.nombre, self.correo, self.contrasena, rol_id),
        )
        mysqlConn.commit()
        self.usuario_id = cleverCursor.lastrowid
        print(f"Usuario '{self.nombre}' guardado con ID {self.usuario_id}")

        if self.rol == "aspirante":
            self.crear_perfil()
        
        
        
#------------------------------------------------------------------------------------------------------------------
def menu():
    while True:
        print("\n--- Menú ---")
        print("1. Crear Usuario")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre completo: ")
            correo = input("Ingrese el correo electrónico: ")
            contrasena = input("Ingrese la contraseña: ")
            rol = input("Ingrese el rol (aspirante/consultor): ")

            usuario = Usuario(nombre, correo, contrasena, rol)
            usuario.guardar_usuario()

        elif opcion == "2":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")
            
if __name__ == "__main__":
    menu()