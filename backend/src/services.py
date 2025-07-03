## aqui definimos que hacen las cosas
import json
import os
from modelos import Evento, Usuario # Importamos las clases que definiste

class GestorEventos:
    """Clase principal que orquesta todo el sistema."""
    def __init__(self):
        self.eventos = []
        self.usuarios = []
        self.ruta_eventos = "data/eventos.json"
        self.ruta_usuarios = "data/usuarios.json"
        os.makedirs("data", exist_ok=True)

        self._cargar_datos()

    def _cargar_datos(self):
        """Carga los datos desde los ficheros JSON al iniciar."""
        try:
            with open(self.ruta_eventos, 'r') as f:
                eventos_data = json.load(f)
                # Convertimos los diccionarios de nuevo a objetos Evento
                self.eventos = [Evento(**data) for data in eventos_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.eventos = [] # Si el fichero no existe o está vacío

        try:
            with open(self.ruta_usuarios, 'r') as f:
                usuarios_data = json.load(f)
                self.usuarios = [Usuario(**data) for data in usuarios_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.usuarios = []

        def _guardar_datos(self):
        """Guarda el estado actual de los datos en los ficheros JSON."""
        with open(self.ruta_eventos, 'w') as f:
            # Convertimos la lista de objetos a una lista de diccionarios
            json.dump([evento.__dict__ for evento in self.eventos], f, indent=4)

        with open(self.ruta_usuarios, 'w') as f:
            json.dump([usuario.__dict__ for usuario in self.usuarios], f, indent=4)

    
    #     deben llamar a self._guardar_datos() al final.

    # --- Tareas para el Rol 2: Desarrollador de Eventos ---
    def registrar_evento(self, nombre, fecha, tipo_evento):
        # El código será implementado por el Desarrollador de Eventos

        eventos_deportivos = {}

        print("\nBienvenido al Gestor Deportivo\n")

        while True:
            print("\nIngrese una de las siguientes opciones:\n")
            print("1. Agregar Nuevo Evento.")
            print("2. Ver Eventos Registrados.")
            print("3. Agregar Nuevo Participante.")

            opcion = int(input())

            if opcion == 1:

                print("\nIngrese los siguientes Datos del Evento:")

                descripcion_evento = {}

                nombre = input("Nombre: ").strip()

                if nombre in eventos_deportivos:
                    print(f"El nombre del evento {nombre} ya esta registrado, por favor ingrese uno nuevo." )
                    continue

                fecha = input("Fecha (ej. DD-MM-AA): ").strip()
                descripcion_evento["Fecha"] = fecha
            
                tipo_evento = input("Tipo de Evento (ej. Futbol, Tenis, etc): ").strip()
                descripcion_evento["Tipo Evento"] = tipo
            
                estado = input("Estado (Confirmado, En proceso, Cancelado): ").strip().lower()
                
                if estado not in ["confirmado", "en proceso", "cancelado"]:
                    print("\nPor favor ingresar el Estado en en su formato válido. 'Confirmado, 'En Proceso', 'Cancelado'\n")
                    continue
                descripcion_evento["Estado"] = estado

                eventos_deportivos[nombre] = descripcion_evento
                print(f"\nEvento {nombre} fue agregado exitosamente.")
            
            elif opcion == 2:

                if not eventos_deportivos:
                    print("No hay Eventos Deportivos Registrados")
                    continue
                
                else:
                    for nombre, datos_evento in eventos_deportivos.items():
                        print(f"\nEvento: {nombre_evento}")
                        print(f"  Fecha: {datos_evento['Fecha']}")
                        print(f"  Tipo: {datos_evento['Tipo Evento']}")
                        print(f"  Estado: {datos_evento['Estado']}")

            if opcion == 3:
                continue
                print("Ingrese los Datos del Nuevo Participante")

    if __name__ == "__main__":
        registrar_evento()




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
