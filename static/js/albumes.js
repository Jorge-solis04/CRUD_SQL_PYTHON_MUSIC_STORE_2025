document.addEventListener('DOMContentLoaded', function() {
  // Datos de ejemplo
  const albumesEjemplo = [
    {
      id: 1,
      titulo: "Thriller",
      artista: "Michael Jackson",
      anio: 1982,
      genero: "Pop",
      disquera: "Epic Records"
    },
    {
      id: 2,
      titulo: "The Dark Side of the Moon",
      artista: "Pink Floyd",
      anio: 1973,
      genero: "Rock Progresivo",
      disquera: "Harvest Records"
    }
  ];

  // Cargar álbumes de ejemplo
  albumesEjemplo.forEach(album => {
    agregarAlbumDOM(album);
  });

  // Manejar el formulario
  const formAlbum = document.getElementById('formAlbum');
  formAlbum.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const nuevoAlbum = {
      id: Date.now(),
      titulo: document.getElementById('titulo').value,
      artista: document.getElementById('artista').value,
      anio: document.getElementById('anio').value,
      genero: document.getElementById('genero').value,
      disquera: document.getElementById('disquera').value
    };
    
    agregarAlbumDOM(nuevoAlbum);
    formAlbum.reset();
  });
});

function agregarAlbumDOM(album) {
  const listaAlbumes = document.getElementById('listaAlbumes');
  
  const albumDiv = document.createElement('div');
  albumDiv.className = 'info-album';
  albumDiv.dataset.id = album.id;
  
  albumDiv.innerHTML = `
    <div class="datos">
      <h3><i class="fas fa-compact-disc"></i> ${album.titulo}</h3>
      <div class="info-item">
        <i class="fas fa-user"></i>
        <p><strong>Artista:</strong> <span class="album-artist">${album.artista}</span></p>
      </div>
      <div class="info-item">
        <i class="fas fa-calendar-alt"></i>
        <p><strong>Año:</strong> ${album.anio}</p>
      </div>
      <div class="info-item">
        <i class="fas fa-music"></i>
        <p><strong>Género:</strong> <span class="genre-tag">${album.genero}</span></p>
      </div>
      <div class="info-item">
        <i class="fas fa-record-vinyl"></i>
        <p><strong>Disquera:</strong> <span class="record-label">${album.disquera}</span></p>
      </div>
    </div>
    <div class="botones">
      <button onclick="editarAlbum(${album.id})" class="btn-edit">
        <i class="fas fa-edit"></i> Editar
      </button>
      <button onclick="borrarAlbum(${album.id})" class="btn-delete">
        <i class="fas fa-trash-alt"></i> Borrar
      </button>
    </div>
  `;
  
  listaAlbumes.appendChild(albumDiv);
}

function editarAlbum(id) {
  const albumDiv = document.querySelector(`.info-album[data-id="${id}"]`);
  
  // Simulación de edición con animación
  albumDiv.style.transform = "scale(0.98)";
  albumDiv.style.boxShadow = "0 0 10px rgba(74, 144, 226, 0.5)";

  setTimeout(() => {
    albumDiv.style.transform = "scale(1)";
    albumDiv.style.boxShadow = "none";
    alert("Modo edición activado para el álbum ID: " + id);
  }, 300);
}

function borrarAlbum(id) {
  if (confirm("¿Estás seguro de borrar este álbum?")) {
    const albumDiv = document.querySelector(`.info-album[data-id="${id}"]`);
    albumDiv.style.animation = "fadeOut 0.5s forwards";

    setTimeout(() => {
      albumDiv.remove();
    }, 500);
  }
}