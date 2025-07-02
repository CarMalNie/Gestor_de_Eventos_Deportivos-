## aqui definimos la estructura de los objetos que vamos a usar
import uuid # Para generar IDs únicos para eventos y usuarios

class Usuario:
    """Representa a un participante del evento."""
    def __init__(self, nombre):
        self.id_usuario = str(uuid.uuid4())[:4] # ID único de 4 caracteres
        self.nombre = nombre

    def __repr__(self):
        # Esta es una forma útil de imprimir la información del objeto
        return f"Usuario(ID: {self.id_usuario}, Nombre: {self.nombre})"

class Evento:
    """Representa un evento deportivo."""
    def __init__(self, nombre, fecha, tipo_evento):
        self.id_evento = str(uuid.uuid4())[:4] # ID único de 4 caracteres
        self.nombre = nombre
        self.fecha = fecha
        self.tipo_evento = tipo_evento
        self.estado = "Pendiente"  # Estados posibles: Pendiente, Confirmado, En Proceso, Cancelado
        self.participantes_inscritos = [] # Lista de IDs de usuarios inscritos
        self.participantes_confirmados = [] # Lista de IDs de usuarios con asistencia confirmada
        self.equipos = {} # Diccionario para almacenar los equipos. Ej: {"Equipo A": [], "Equipo B": []}

    def __repr__(self):
        return f"Evento(ID: {self.id_evento}, Nombre: '{self.nombre}', Estado: {self.estado})"
