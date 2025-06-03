document.addEventListener('DOMContentLoaded', function() {
  // Datos de ejemplo
  const artistasEjemplo = [
    { id: 1, nombre: "Michael Jackson" },
    { id: 2, nombre: "Pink Floyd" },
    { id: 3, nombre: "The Beatles" }
  ];

  // Cargar artistas de ejemplo
  artistasEjemplo.forEach(artista => {
    agregarArtistaDOM(artista);
  });

  // Manejar el formulario
  const formArtista = document.getElementById('formArtista');
  formArtista.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const nuevoArtista = {
      id: Date.now(),
      nombre: document.getElementById('nombre').value
    };
    
    agregarArtistaDOM(nuevoArtista);
    formArtista.reset();
  });
});

function agregarArtistaDOM(artista) {
  const tablaArtistas = document.querySelector('#tablaArtistas tbody');
  
  const fila = document.createElement('tr');
  fila.dataset.id = artista.id;
  
  fila.innerHTML = `
    <td>${artista.nombre}</td>
    <td class="acciones">
      <button onclick="editarArtista(${artista.id})" class="btn-edit">
        <i class="fas fa-edit"></i> Editar
      </button>
      <button onclick="borrarArtista(${artista.id})" class="btn-delete">
        <i class="fas fa-trash-alt"></i> Borrar
      </button>
    </td>
  `;
  
  tablaArtistas.appendChild(fila);
}

function editarArtista(id) {
  const fila = document.querySelector(`tr[data-id="${id}"]`);
  
  // Simulación de edición con animación
  fila.style.transform = "scale(0.98)";
  fila.style.boxShadow = "0 0 10px rgba(74, 144, 226, 0.5)";

  setTimeout(() => {
    fila.style.transform = "scale(1)";
    fila.style.boxShadow = "none";
    
    const nombreActual = fila.querySelector('td:first-child').textContent;
    const nuevoNombre = prompt("Editar nombre del artista:", nombreActual);
    
    if (nuevoNombre && nuevoNombre.trim() !== "") {
      fila.querySelector('td:first-child').textContent = nuevoNombre.trim();
    }
  }, 300);
}

function borrarArtista(id) {
  if (confirm("¿Estás seguro de borrar este artista?")) {
    const fila = document.querySelector(`tr[data-id="${id}"]`);
    fila.style.animation = "fadeOut 0.5s forwards";

    setTimeout(() => {
      fila.remove();
    }, 500);
  }
}