# --------------------------------------------------------------------------
# services.py - Lógica de Negocio del Gestor de Eventos
# --------------------------------------------------------------------------
# Este fichero contiene la clase `GestorEventos`, que encapsula toda la
# lógica para manejar eventos, usuarios, inscripciones y equipos.
# Es el "cerebro" de la aplicación, separando las operaciones de la
# capa de presentación (API).
# --------------------------------------------------------------------------

import json
import os
import random
from pathlib import Path
from typing import List, Optional
from .models import Evento, Usuario, EstadoEvento
import threading

class GestorEventos:
    """
    Clase principal que orquesta todo el sistema.
    Maneja la carga, guardado y manipulación de datos.
    """
    def __init__(self):
        self.eventos: List[Evento] = []
        self.usuarios: List[Usuario] = []
        # Usar Path para manejar rutas de manera segura y compatible entre sistemas operativos
        self.base_path = Path(os.path.dirname(os.path.dirname(__file__))) / "data"
        self.ruta_eventos = self.base_path / "eventos.json"
        self.ruta_usuarios = self.base_path / "usuarios.json"
        self.lock = threading.Lock()  # Para operaciones seguras en entornos multi-hilo

        # Asegurar que el directorio 'data' existe al iniciar
        self.base_path.mkdir(exist_ok=True)
        self._cargar_datos()

    def _cargar_datos(self):
        """
        Carga los datos desde los ficheros JSON al iniciar la aplicación.
        Si los ficheros no existen o están vacíos, se inicializan listas vacías.
        """
        with self.lock:
            try:
                if self.ruta_eventos.exists() and self.ruta_eventos.stat().st_size > 0:
                    with open(self.ruta_eventos, 'r', encoding='utf-8') as f:
                        eventos_data = json.load(f)
                        self.eventos = [Evento.model_validate(data) for data in eventos_data]
                else:
                    self.eventos = []
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error al cargar eventos: {e}")
                self.eventos = []

            try:
                if self.ruta_usuarios.exists() and self.ruta_usuarios.stat().st_size > 0:
                    with open(self.ruta_usuarios, 'r', encoding='utf-8') as f:
                        usuarios_data = json.load(f)
                        self.usuarios = [Usuario.model_validate(data) for data in usuarios_data]
                else:
                    self.usuarios = []
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error al cargar usuarios: {e}")
                self.usuarios = []

    def _guardar_datos(self):
        """
        Guarda el estado actual de los datos (eventos y usuarios)
        en sus respectivos ficheros JSON.
        """
        with self.lock:
            with open(self.ruta_eventos, 'w', encoding='utf-8') as f:
                json.dump([evento.model_dump() for evento in self.eventos], f, indent=4, ensure_ascii=False)
            with open(self.ruta_usuarios, 'w', encoding='utf-8') as f:
                json.dump([usuario.model_dump() for usuario in self.usuarios], f, indent=4, ensure_ascii=False)

    def _generar_id_unico(self, tipo: str) -> str:
        """Genera un ID único de 4 dígitos que no exista en la lista correspondiente."""
        if tipo == "evento":
            ids_existentes = {e.id_evento for e in self.eventos}
        else:
            ids_existentes = {u.id_usuario for u in self.usuarios}
        
        while True:
            nuevo_id = str(random.randint(1000, 9999))
            if nuevo_id not in ids_existentes:
                return nuevo_id

   

    def registrar_evento(self, nombre: str, fecha: str, tipo_evento: str) -> Evento:
        """Registra un nuevo evento en el sistema con un ID único."""
        id_unico = self._generar_id_unico("evento")
        evento = Evento(id_evento=id_unico, nombre=nombre, fecha=fecha, tipo_evento=tipo_evento)
        self.eventos.append(evento)
        self._guardar_datos()
        return evento

    def consultar_eventos_por_estado(self, estado: str) -> List[Evento]:
        """Filtra y devuelve los eventos que coinciden con un estado dado."""
        return [evento for evento in self.eventos if evento.estado.lower() == estado.lower()]

    def actualizar_estado_evento(self, id_evento: str, nuevo_estado: str) -> Optional[Evento]:
        """Actualiza el estado de un evento específico."""
        for evento in self.eventos:
            if evento.id_evento == id_evento:
                if evento.actualizar_estado(nuevo_estado):
                    self._guardar_datos()
                    return evento
        return None


    def registrar_usuario(self, nombre: str) -> Usuario:
        """Registra un nuevo usuario en el sistema con un ID único."""
        id_unico = self._generar_id_unico("usuario")
        usuario = Usuario(id_usuario=id_unico, nombre=nombre)
        self.usuarios.append(usuario)
        self._guardar_datos()
        return usuario

    def inscribir_usuario_en_evento(self, id_usuario: str, id_evento: str) -> bool:
        """Inscribe un usuario en un evento si ambos existen."""
        evento = next((e for e in self.eventos if e.id_evento == id_evento), None)
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)

        if evento and usuario:
            if id_usuario not in evento.participantes_inscritos:
                evento.participantes_inscritos.append(id_usuario)
                self._guardar_datos()
                return True
        return False

    def confirmar_asistencia(self, id_usuario: str, id_evento: str) -> bool:
        """Confirma la asistencia de un usuario a un evento."""
        evento = next((e for e in self.eventos if e.id_evento == id_evento), None)
        if evento and id_usuario in evento.participantes_inscritos:
            if id_usuario not in evento.participantes_confirmados:
                evento.participantes_confirmados.append(id_usuario)
                self._guardar_datos()
                return True
        return False

   

    def asignar_equipos(self, id_evento: str) -> Optional[Evento]:
        """Asigna aleatoriamente los participantes confirmados a dos equipos."""
        evento = next((e for e in self.eventos if e.id_evento == id_evento), None)
        if not evento or not evento.participantes_confirmados:
            return None

        participantes = list(evento.participantes_confirmados)
        random.shuffle(participantes)
        
        mitad = len(participantes) // 2
        equipo_a = participantes[:mitad]
        equipo_b = participantes[mitad:]

        evento.equipos = {
            "Equipo A": equipo_a,
            "Equipo B": equipo_b
        }
        self._guardar_datos()
        return evento

    def consultar_equipos_de_evento(self, id_evento: str) -> Optional[dict]:
        """Devuelve los equipos asignados para un evento."""
        evento = next((e for e in self.eventos if e.id_evento == id_evento), None)
        return evento.equipos if evento else None
