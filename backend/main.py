# --------------------------------------------------------------------------
# main.py - Servidor Principal de la API con FastAPI
# --------------------------------------------------------------------------
# Este fichero es el punto de entrada para el backend. Define todas las
# rutas (endpoints) de la API que el frontend consumirá.
# --------------------------------------------------------------------------

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator, Field
from typing import List
from datetime import datetime
import os

# Importamos la lógica de negocio y los modelos de datos
from src.services import GestorEventos
from src.models import Evento, Usuario, EstadoEvento, TipoEvento

# --- Modelos Pydantic para la validación de datos de entrada ---
# FastAPI usará estos modelos para validar automáticamente los datos
# que lleguen en las peticiones (POST, PUT, etc.).

class EventoCrear(BaseModel):
    nombre: str = Field(..., min_length=3, description="Nombre del evento, mínimo 3 caracteres")
    fecha: str = Field(..., description="Fecha del evento en formato YYYY-MM-DD")
    tipo_evento: str = Field(..., description="Tipo de evento deportivo")

    @validator('fecha')
    def validar_fecha(cls, v):
        try:
            fecha = datetime.strptime(v, "%Y-%m-%d")
            if fecha < datetime.now():
                raise ValueError("La fecha no puede ser en el pasado")
            return v
        except ValueError as e:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")

    @validator('tipo_evento')
    def validar_tipo_evento(cls, v):
        if v not in [t.value for t in TipoEvento]:
            raise ValueError(f"Tipo de evento inválido. Valores permitidos: {[t.value for t in TipoEvento]}")
        return v

class UsuarioCrear(BaseModel):
    nombre: str = Field(..., min_length=2, description="Nombre del usuario, mínimo 2 caracteres")

class Inscripcion(BaseModel):
    id_usuario: str = Field(..., description="ID del usuario a inscribir")
    id_evento: str = Field(..., description="ID del evento")

class EstadoUpdate(BaseModel):
    nuevo_estado: str = Field(..., description="Nuevo estado del evento")

    @validator('nuevo_estado')
    def validar_estado(cls, v):
        if v not in [e.value for e in EstadoEvento]:
            raise ValueError(f"Estado inválido. Valores permitidos: {[e.value for e in EstadoEvento]}")
        return v


# --- Inicialización de la Aplicación ---

app = FastAPI(
    title="API del Gestor de Eventos Deportivos",
    description="API para gestionar eventos, inscripciones y equipos.",
    version="1.0.0"
)

# Se crea una única instancia del gestor que manejará toda la lógica.
gestor = GestorEventos()

# --- Configuración de CORS ---
# Permite que el frontend (que corre en un origen diferente) pueda
# hacer peticiones a este backend. Es un ajuste de seguridad crucial.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)


# --- Endpoints de la API ---

## Endpoints para Eventos
# -------------------------------------------------

@app.get("/api/eventos", response_model=List[Evento], tags=["Eventos"])
def obtener_todos_los_eventos():
    """
    Obtiene una lista de todos los eventos registrados.
    """
    return gestor.eventos

@app.post("/api/eventos", response_model=Evento, status_code=status.HTTP_201_CREATED, tags=["Eventos"])
def crear_nuevo_evento(evento_data: EventoCrear):
    """
    Registra un nuevo evento en el sistema.
    """
    nuevo_evento = gestor.registrar_evento(
        evento_data.nombre,
        evento_data.fecha,
        evento_data.tipo_evento
    )
    return nuevo_evento

@app.put("/api/eventos/{id_evento}/estado", response_model=Evento, tags=["Eventos"])
def actualizar_estado_evento(id_evento: str, estado_data: EstadoUpdate):
    """
    Actualiza el estado de un evento específico (ej. a 'Confirmado').
    """
    evento_actualizado = gestor.actualizar_estado_evento(id_evento, estado_data.nuevo_estado)
    if not evento_actualizado:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento_actualizado

@app.get("/api/eventos/estado/{estado}", response_model=List[Evento], tags=["Eventos"])
def obtener_eventos_por_estado(estado: str):
    """
    Filtra y devuelve eventos según su estado.
    """
    return gestor.consultar_eventos_por_estado(estado)

## Endpoints para Usuarios
# -------------------------------------------------

@app.get("/api/usuarios", response_model=List[Usuario], tags=["Usuarios"])
def obtener_todos_los_usuarios():
    """
    Obtiene una lista de todos los usuarios registrados.
    """
    return gestor.usuarios

@app.post("/api/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def crear_nuevo_usuario(usuario_data: UsuarioCrear):
    """
    Registra un nuevo usuario en el sistema.
    """
    return gestor.registrar_usuario(usuario_data.nombre)


## Endpoints para Inscripciones y Equipos
# -------------------------------------------------

@app.post("/api/inscripciones", status_code=status.HTTP_201_CREATED, tags=["Inscripciones y Equipos"])
def inscribir_usuario(inscripcion_data: Inscripcion):
    """
    Inscribe un usuario en un evento.
    """
    resultado = gestor.inscribir_usuario_en_evento(
        inscripcion_data.id_usuario,
        inscripcion_data.id_evento
    )
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario o Evento no encontrado")
    return {"mensaje": "Usuario inscrito correctamente"}

@app.put("/api/inscripciones/confirmar", tags=["Inscripciones y Equipos"])
def confirmar_asistencia_usuario(inscripcion_data: Inscripcion):
    """
    Confirma la asistencia de un participante a un evento.
    """
    resultado = gestor.confirmar_asistencia(
        inscripcion_data.id_usuario,
        inscripcion_data.id_evento
    )
    if not resultado:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return {"mensaje": "Asistencia confirmada"}


@app.post("/api/eventos/{id_evento}/equipos", tags=["Inscripciones y Equipos"])
def asignar_equipos_evento(id_evento: str):
    """
    Asigna automáticamente los equipos para un evento.
    """
    evento = gestor.asignar_equipos(id_evento)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado o sin participantes confirmados")
    return {"mensaje": "Equipos asignados correctamente", "equipos": evento.equipos}


