document.addEventListener('DOMContentLoaded', function() {
  // Mostrar/ocultar contraseña (si aplica)
  const showPassword = document.getElementById('showPassword');
  if (showPassword) {
    showPassword.addEventListener('click', function() {
      const passwordField = document.getElementById('password');
      if (passwordField.type === 'password') {
        passwordField.type = 'text';
        this.innerHTML = '<i class="far fa-eye-slash"></i>';
      } else {
        passwordField.type = 'password';
        this.innerHTML = '<i class="far fa-eye"></i>';
      }
    });
  }

  // Filtrar productos
  const tipoProductoFilter = document.getElementById('tipo-producto');
  if (tipoProductoFilter) {
    tipoProductoFilter.addEventListener('change', function() {
      const tipo = this.value;
      const productos = document.querySelectorAll('.info-cliente');
      
      productos.forEach(producto => {
        const tipoProducto = producto.querySelector('.fa-tag + span').textContent.toLowerCase();
        if (tipo === 'todos' || tipoProducto.includes(tipo)) {
          producto.style.display = 'block';
        } else {
          producto.style.display = 'none';
        }
      });
    });
  }

  // Manejar el formulario de producto
  const formProducto = document.getElementById('formProducto');
  if (formProducto) {
    formProducto.addEventListener('submit', function(e) {
      e.preventDefault();
      // Aquí iría la lógica para agregar el producto
      alert('Producto agregado (esta es una simulación)');
      this.reset();
    });
  }

  // Manejar botones de editar/eliminar
  document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', function() {
      // Lógica para editar producto
      alert('Editar producto (simulación)');
    });
  });

  document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', function() {
      if (confirm('¿Estás seguro de eliminar este producto?')) {
        this.closest('.info-cliente').remove();
      }
    });
  });
});