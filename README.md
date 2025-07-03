# Gestor de Eventos Deportivos

## Descripción General

Este proyecto es una aplicación web diseñada para facilitar la gestión de eventos deportivos. Permite a los usuarios crear eventos, registrar participantes e inscribirlos en diferentes actividades. La aplicación cuenta con un backend desarrollado en Python con FastAPI y un frontend interactivo y responsivo construido con HTML, CSS, JavaScript y Bootstrap.

## Características Principales

- **Gestión de Eventos**: Crear, ver y filtrar eventos por estado (Pendiente, Confirmado, etc.).
- **Gestión de Usuarios**: Registrar nuevos usuarios en el sistema.
- **Inscripciones**: Inscribir usuarios en los eventos desde una interfaz modal detallada.
- **Asignación de Equipos**: Asignar automáticamente los participantes inscritos a dos equipos (Equipo A y Equipo B).
- **Interfaz Responsiva**: El diseño se adapta a diferentes tamaños de pantalla, desde móviles a ordenadores de escritorio, gracias a Bootstrap.
- **Feedback al Usuario**: Alertas visuales para confirmar acciones como la creación de eventos o la inscripción de usuarios.
- **ID Únicos**: El backend genera un ID numérico único de 4 dígitos para cada evento y usuario, evitando colisiones.

## Arquitectura del Proyecto

La aplicación sigue una arquitectura cliente-servidor desacoplada.

### Backend

- **Framework**: FastAPI.
- **Lógica de Negocio**: La clase `GestorEventos` en `src/services.py` centraliza toda la lógica, incluyendo la generación de IDs únicos para evitar duplicados.
- **Modelos de Datos**: Las clases en `src/models.py` usan Pydantic para la validación de datos.
- **Persistencia**: Los datos se guardan en ficheros `eventos.json` y `usuarios.json` en el directorio `data/`.

### Frontend

- **Tecnologías**: HTML, CSS, JavaScript y Bootstrap 5.
- **Interfaz de Usuario**: El diseño se basa en tarjetas para mostrar los eventos y utiliza un modal para los detalles, inscripciones y asignación de equipos.
- **Interactividad**: El fichero `js/main.js` maneja las llamadas a la API, la actualización dinámica del DOM y la gestión de eventos del usuario.

## Estructura de Datos (JSON)

Los datos se almacenan en un formato JSON limpio y legible.

### `eventos.json`

```json
[
    {
        "id_evento": "1234",
        "nombre": "Torneo de Voleibol",
        "fecha": "2025-08-15",
        "tipo_evento": "Voleibol",
        "estado": "Pendiente",
        "participantes_inscritos": ["5678"],
        "participantes_confirmados": [],
        "equipos": {}
    }
]
```

### `usuarios.json`

```json
[
    {
        "id_usuario": "5678",
        "nombre": "Ana García"
    }
]
```

## Cómo Ejecutar la Aplicación

1.  **Backend**:
    - Navega al directorio `backend`.
    - Instala las dependencias: `pip install -r requirements.txt`.
    - Inicia el servidor: `uvicorn main:app --reload`.
    - La API estará disponible en `http://127.0.0.1:8000`.

2.  **Frontend**:
    - Abre el fichero `frontend/index.html` en tu navegador web.

