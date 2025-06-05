document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const passwordInput = document.getElementById('password');
    

    

    // Validación del formulario
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Obtener valores
        const username = document.getElementById('username').value.trim();
        const password = passwordInput.value.trim();
        const remember = document.querySelector('input[name="remember"]').checked;
        
        // Validar campos
        let isValid = true;
        
        if (username === '') {
            showError('username', 'Por favor ingresa tu usuario o email');
            isValid = false;
        } else if (!isValidEmail(username) && !isValidUsername(username)) {
            showError('username', 'Ingresa un usuario o email válido');
            isValid = false;
        }
        
        if (password === '') {
            showError('password', 'Por favor ingresa tu contraseña');
            isValid = false;
        } else if (password.length < 6) {
            showError('password', 'La contraseña debe tener al menos 6 caracteres');
            isValid = false;
        }
        
        // Si todo es válido
        if (isValid) {
            // Simular envío al servidor
            console.log('Datos del login:', { username, password, remember });
            
            // Mostrar animación de carga
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verificando...';
            submitBtn.disabled = true;
            
            // Simular retardo de red
            setTimeout(() => {
                // Éxito (en un caso real, redirigir o mostrar mensaje del servidor)
                showSuccessMessage();
                
                // Restaurar botón
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 1500);
        }
    });
    
    function isValidUsername(username) {
        const re = /^[a-zA-Z0-9_]{4,20}$/;
        return re.test(username);
    }
    
    function showError(fieldId, message) {
        const field = document.getElementById(fieldId);
        let errorElement = field.nextElementSibling;
        
        // Si no existe el elemento de error, lo creamos
        if (!errorElement || !errorElement.classList.contains('error-message')) {
            errorElement = document.createElement('div');
            errorElement.className = 'error-message';
            field.parentNode.insertBefore(errorElement, field.nextSibling);
        }
        
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        
        // Resaltar el campo con error
        field.style.borderColor = '#e74c3c';
        field.style.backgroundColor = '#fff0f0';
        
        // Quitar el error cuando el usuario empiece a escribir
        field.addEventListener('input', function() {
            errorElement.style.display = 'none';
            field.style.borderColor = '#e0e0e0';
            field.style.backgroundColor = '#f9f9f9';
        }, { once: true });
    }

    // Dummy function for email validation (add your own logic if needed)
    function isValidEmail(email) {
        // Simple email regex
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Dummy function for success message (implement as needed)
    function showSuccessMessage() {
        alert('¡Inicio de sesión exitoso!');
    }
    
});