## aqui definimos que hacen las cosas
from modelos import Evento, Usuario # Importamos las clases que definiste

class GestorEventos:
    """Clase principal que orquesta todo el sistema."""
    def __init__(self):
        self.eventos = []
        self.usuarios = []

    # --- Tareas para el Rol 2: Desarrollador de Eventos ---
    def registrar_evento(self, nombre, fecha, tipo_evento):
        # El código será implementado por el Desarrollador de Eventos
        pass

    def consultar_eventos_por_estado(self, estado):
        # El código será implementado por el Desarrollador de Eventos
        pass

    def actualizar_estado_evento(self, id_evento, nuevo_estado):
        # El código será implementado por el Desarrollador de Eventos
        pass

    # --- Tareas para el Rol 3: Desarrollador de Usuarios e Inscripciones ---
    def registrar_usuario(self, nombre):
        # El código será implementado por el Desarrollador de Usuarios
        pass
        
    def inscribir_usuario_en_evento(self, id_usuario, id_evento):
        # El código será implementado por el Desarrollador de Usuarios
        pass
        
    def confirmar_asistencia(self, id_usuario, id_evento):
        # El código será implementado por el Desarrollador de Usuarios
        pass

    # --- Tareas para el Rol 4: Desarrollador de Lógica de Equipos ---
    def asignar_equipos(self, id_evento):
        # El código será implementado por el Desarrollador de Equipos
        pass
        
    def consultar_equipos_de_evento(self, id_evento):
        # El código será implementado por el Desarrollador de Equipos
        pass
