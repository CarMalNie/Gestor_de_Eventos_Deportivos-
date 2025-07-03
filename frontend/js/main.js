const API_URL = 'http://127.0.0.1:8000';
let modalDetalles = null; // Variable global para la instancia del modal

document.addEventListener('DOMContentLoaded', () => {
    // Inicializar la instancia del modal de Bootstrap
    modalDetalles = new bootstrap.Modal(document.getElementById('modal-detalles-evento'));

    // Cargar datos iniciales
    cargarEventos();
    cargarUsuarios();

    // Asignar eventos a los formularios y filtros
    document.getElementById('form-crear-evento').addEventListener('submit', crearEvento);
    document.getElementById('form-crear-usuario').addEventListener('submit', crearUsuario);
    document.getElementById('form-inscribir-usuario').addEventListener('submit', inscribirUsuario);
    document.getElementById('filtro-estado').addEventListener('change', cargarEventos);
});

// Muestra una alerta temporal en la UI
function mostrarAlerta(mensaje, tipo = 'success') {
    const placeholder = document.getElementById('alerta-placeholder');
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
        <div class="alert alert-${tipo} alert-dismissible fade show" role="alert">
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    placeholder.append(wrapper);

    // Eliminar la alerta después de 3 segundos
    setTimeout(() => wrapper.remove(), 3000);
}

// Carga los eventos desde la API y los muestra como tarjetas
async function cargarEventos() {
    const filtro = document.getElementById('filtro-estado').value;
    let url = `${API_URL}/api/eventos`;
    if (filtro !== 'todos') {
        url = `${API_URL}/api/eventos/estado/${filtro}`;
    }

    try {
        const response = await fetch(url);
        const eventos = await response.json();
        const listaEventos = document.getElementById('lista-eventos');
        listaEventos.innerHTML = '';

        if (eventos.length === 0) {
            listaEventos.innerHTML = '<p class="text-muted">No hay eventos que coincidan con el filtro.</p>';
            return;
        }

        eventos.forEach(evento => {
            const col = document.createElement('div');
            col.className = 'col-md-6 mb-4';
            col.innerHTML = `
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${evento.nombre}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">${evento.tipo_evento}</h6>
                        <p class="card-text">Fecha: ${evento.fecha}</p>
                        <span class="badge bg-info text-dark">${evento.estado}</span>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-sm btn-outline-primary" onclick="mostrarDetallesEvento('${evento.id_evento}')">
                            Ver Detalles
                        </button>
                    </div>
                </div>
            `;
            listaEventos.appendChild(col);
        });
    } catch (error) {
        console.error('Error al cargar eventos:', error);
    }
}

// Carga la lista de usuarios registrados
async function cargarUsuarios() {
    try {
        const response = await fetch(`${API_URL}/api/usuarios`);
        const usuarios = await response.json();
        const listaUsuarios = document.getElementById('lista-usuarios');
        listaUsuarios.innerHTML = '';
        usuarios.forEach(usuario => {
            const item = document.createElement('div');
            item.className = 'list-group-item';
            item.textContent = `${usuario.nombre} (ID: ${usuario.id_usuario})`;
            listaUsuarios.appendChild(item);
        });
    } catch (error) {
        console.error('Error al cargar usuarios:', error);
    }
}

// Muestra el modal con los detalles de un evento
async function mostrarDetallesEvento(id_evento) {
    try {
        const [evento, usuarios] = await Promise.all([
            fetch(`${API_URL}/api/eventos`).then(res => res.json()).then(eventos => eventos.find(e => e.id_evento === id_evento)),
            fetch(`${API_URL}/api/usuarios`).then(res => res.json())
        ]);

        document.getElementById('modal-titulo-evento').textContent = evento.nombre;
        document.getElementById('id-evento-inscribir').value = id_evento;

        // Poblar el selector con usuarios no inscritos
        const selectUsuario = document.getElementById('select-usuario-inscribir');
        selectUsuario.innerHTML = '';
        const usuariosNoInscritos = usuarios.filter(u => !evento.participantes_inscritos.includes(u.id_usuario));
        usuariosNoInscritos.forEach(usuario => {
            const option = document.createElement('option');
            option.value = usuario.id_usuario;
            option.textContent = usuario.nombre;
            selectUsuario.appendChild(option);
        });

        // Mostrar participantes inscritos
        const listaParticipantes = document.getElementById('lista-participantes-inscritos');
        listaParticipantes.innerHTML = '';
        evento.participantes_inscritos.forEach(id_usuario => {
            const usuario = usuarios.find(u => u.id_usuario === id_usuario);
            if (usuario) {
                const item = document.createElement('li');
                item.className = 'list-group-item';
                item.textContent = usuario.nombre;
                listaParticipantes.appendChild(item);
            }
        });

        // Asignar evento al botón de equipos y mostrar equipos
        document.getElementById('btn-asignar-equipos').onclick = () => asignarEquipos(id_evento);
        mostrarEquipos(evento, usuarios);

        modalDetalles.show();
    } catch (error) {
        console.error('Error al mostrar detalles:', error);
    }
}

// Muestra los equipos si ya han sido asignados
function mostrarEquipos(evento, usuarios) {
    const contenedorEquipos = document.getElementById('equipos-asignados');
    contenedorEquipos.innerHTML = '';
    if (Object.keys(evento.equipos).length > 0) {
        let html = '<h6>Equipos Asignados</h6>';
        for (const equipo in evento.equipos) {
            html += `<strong>${equipo}:</strong><ul>`;
            evento.equipos[equipo].forEach(id_usuario => {
                const usuario = usuarios.find(u => u.id_usuario === id_usuario);
                if (usuario) {
                    html += `<li>${usuario.nombre}</li>`;
                }
            });
            html += '</ul>';
        }
        contenedorEquipos.innerHTML = html;
    }
}

// --- ACCIONES ---

async function crearEvento(e) {
    e.preventDefault();
    const evento = {
        nombre: document.getElementById('nombre-evento').value,
        fecha: document.getElementById('fecha-evento').value,
        tipo_evento: document.getElementById('tipo-evento').value,
    };
    await fetch(`${API_URL}/api/eventos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(evento),
    });
    mostrarAlerta('Evento creado con éxito.');
    cargarEventos();
    e.target.reset();
}

async function crearUsuario(e) {
    e.preventDefault();
    const usuario = { nombre: document.getElementById('nombre-usuario').value };
    await fetch(`${API_URL}/api/usuarios`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(usuario),
    });
    mostrarAlerta('Usuario creado con éxito.', 'success');
    cargarUsuarios();
    e.target.reset();
}

async function inscribirUsuario(e) {
    e.preventDefault();
    const id_evento = document.getElementById('id-evento-inscribir').value;
    const id_usuario = document.getElementById('select-usuario-inscribir').value;
    if (!id_usuario) {
        mostrarAlerta('No hay usuarios para inscribir.', 'warning');
        return;
    }
    await fetch(`${API_URL}/api/inscripciones`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_evento, id_usuario }),
    });
    mostrarAlerta('Usuario inscrito correctamente.', 'info');
    // Recargar detalles en el modal para reflejar el cambio
    mostrarDetallesEvento(id_evento);
}

async function asignarEquipos(id_evento) {
    await fetch(`${API_URL}/api/eventos/${id_evento}/equipos`, { method: 'POST' });
    mostrarAlerta('Equipos asignados correctamente.');
    mostrarDetallesEvento(id_evento);
}
