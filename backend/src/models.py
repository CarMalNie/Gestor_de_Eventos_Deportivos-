from enum import Enum
from typing import List, Dict
from pydantic import BaseModel, Field

class EstadoEvento(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADO = "Confirmado"
    EN_PROCESO = "En Proceso"
    CANCELADO = "Cancelado"

class TipoEvento(Enum):
    FUTBOL = "Fútbol"
    BALONCESTO = "Baloncesto"
    VOLEIBOL = "Voleibol"
    TENIS = "Tenis"
    OTRO = "Otro"

class Usuario(BaseModel):
    """Representa a un participante del evento."""
    id_usuario: str
    nombre: str

    class Config:
        from_attributes = True

class Evento(BaseModel):
    """Representa un evento deportivo."""
    id_evento: str
    nombre: str
    fecha: str
    tipo_evento: str
    estado: str = EstadoEvento.PENDIENTE.value
    participantes_inscritos: List[str] = Field(default_factory=list)
    participantes_confirmados: List[str] = Field(default_factory=list)
    equipos: Dict[str, List[str]] = Field(default_factory=dict)

    def actualizar_estado(self, nuevo_estado: str) -> bool:
        """Actualiza el estado del evento si es válido."""
        if nuevo_estado in [e.value for e in EstadoEvento]:
            self.estado = nuevo_estado
            return True
        return False

    class Config:
        from_attributes = True
