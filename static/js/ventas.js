document.addEventListener('DOMContentLoaded', function() {
    // Array para almacenar las ventas
    let ventas = [];
    let ventaIdCounter = 1;

    // Elementos del DOM
    const formVenta = document.getElementById('formVenta');
    const listaVentas = document.getElementById('listaVentas');
    const submitButton = formVenta.querySelector('button[type="submit"]');

    // Función para agregar o actualizar una venta
    function manejarVenta(event) {
        event.preventDefault();
        
        // Obtener valores del formulario
        const fecha = document.getElementById('fecha').value;
        const cliente = document.getElementById('cliente').value;
        const formato = document.getElementById('formato').value;
        const cantidad = document.getElementById('cantidad').value;
        const precio = document.getElementById('precio').value;
        
        // Verificar si estamos editando una venta existente
        const editingId = formVenta.dataset.editingId;
        
        if (editingId) {
            // Actualizar la venta existente
            const ventaIndex = ventas.findIndex(v => v.id === parseInt(editingId));
            if (ventaIndex !== -1) {
                ventas[ventaIndex] = {
                    id: parseInt(editingId),
                    fecha,
                    cliente,
                    formato,
                    cantidad,
                    precio
                };
            }
            
            // Restaurar el botón a su estado original
            submitButton.innerHTML = '<i class="fas fa-plus"></i> Registrar';
            
            // Eliminar el ID de edición
            delete formVenta.dataset.editingId;
        } else {
            // Crear nueva venta
            const venta = {
                id: ventaIdCounter++,
                fecha,
                cliente,
                formato,
                cantidad,
                precio
            };
            
            // Agregar al array
            ventas.push(venta);
        }
        
        // Actualizar la lista y resetear el formulario
        actualizarListaVentas();
        formVenta.reset();
    }

    // Función para actualizar la lista de ventas
    function actualizarListaVentas() {
        // Limpiar la lista
        listaVentas.innerHTML = '';
        
        // Ordenar ventas por fecha (más reciente primero)
        ventas.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
        
        // Agregar cada venta a la lista
        ventas.forEach(venta => {
            const ventaElement = document.createElement('div');
            ventaElement.className = 'info-venta';
            ventaElement.innerHTML = `
                <div class="datos">
                    <h3><i class="fas fa-receipt"></i> Venta #${venta.id}</h3>
                    <div class="info-item">
                        <i class="far fa-calendar-alt"></i>
                        <span class="venta-fecha">${formatearFecha(venta.fecha)}</span>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-user"></i>
                        <span class="venta-cliente">${venta.cliente}</span>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-compact-disc"></i>
                        <span class="formato-tag">${venta.formato}</span>
                        <span> x ${venta.cantidad}</span>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-dollar-sign"></i>
                        <span class="venta-total">$${parseFloat(venta.precio).toFixed(2)}</span>
                    </div>
                </div>
                <div class="botones">
                    <button class="btn-edit" onclick="editarVenta(${venta.id})">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button class="btn-delete" onclick="eliminarVenta(${venta.id})">
                        <i class="fas fa-trash"></i> Eliminar
                    </button>
                </div>
            `;
            
            listaVentas.appendChild(ventaElement);
        });
    }

    // Función para formatear la fecha
    function formatearFecha(fechaString) {
        const opciones = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(fechaString).toLocaleDateString('es-ES', opciones);
    }

    // Función para eliminar una venta
    window.eliminarVenta = function(id) {
        if (confirm('¿Estás seguro de que quieres eliminar esta venta?')) {
            ventas = ventas.filter(venta => venta.id !== id);
            actualizarListaVentas();
            
            // Si estaba en edición, cancelar la edición
            if (formVenta.dataset.editingId && parseInt(formVenta.dataset.editingId) === id) {
                submitButton.innerHTML = '<i class="fas fa-plus"></i> Registrar';
                delete formVenta.dataset.editingId;
                formVenta.reset();
            }
        }
    }

    // Función para editar una venta
    window.editarVenta = function(id) {
        const venta = ventas.find(v => v.id === id);
        if (venta) {
            // Llenar el formulario con los datos de la venta
            document.getElementById('fecha').value = venta.fecha;
            document.getElementById('cliente').value = venta.cliente;
            document.getElementById('formato').value = venta.formato;
            document.getElementById('cantidad').value = venta.cantidad;
            document.getElementById('precio').value = venta.precio;
            
            // Cambiar el texto del botón a "Actualizar"
            submitButton.innerHTML = '<i class="fas fa-sync-alt"></i> Actualizar';
            
            // Guardar el ID de la venta que se está editando
            formVenta.dataset.editingId = id;
            
            // Hacer scroll al formulario para mejor experiencia de usuario
            document.querySelector('.formulario-agregar').scrollIntoView({ behavior: 'smooth' });
        }
    }

    // Establecer fecha predeterminada como hoy
    document.getElementById('fecha').valueAsDate = new Date();

    // Event listener para el formulario
    formVenta.addEventListener('submit', manejarVenta);

    // Cargar algunas ventas de ejemplo
    cargarVentasEjemplo();
    
    function cargarVentasEjemplo() {
        const hoy = new Date();
        const ayer = new Date(hoy);
        ayer.setDate(hoy.getDate() - 1);
        const semanaPasada = new Date(hoy);
        semanaPasada.setDate(hoy.getDate() - 7);
        
        const ventasEjemplo = [
            {
                id: ventaIdCounter++,
                fecha: hoy.toISOString().split('T')[0],
                cliente: "Juan Pérez",
                formato: "Vinilo",
                cantidad: 2,
                precio: 49.98
            },
            {
                id: ventaIdCounter++,
                fecha: ayer.toISOString().split('T')[0],
                cliente: "María García",
                formato: "CD",
                cantidad: 3,
                precio: 35.97
            },
            {
                id: ventaIdCounter++,
                fecha: semanaPasada.toISOString().split('T')[0],
                cliente: "Carlos López",
                formato: "Cassete",
                cantidad: 1,
                precio: 12.99
            }
        ];
        
        ventas = ventasEjemplo;
        actualizarListaVentas();
    }
});