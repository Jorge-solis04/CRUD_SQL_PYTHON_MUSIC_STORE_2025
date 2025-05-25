document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const showPasswordBtn = document.getElementById('showPassword');
    const passwordInput = document.getElementById('password');
    
    // Mostrar/ocultar contraseña
    showPasswordBtn.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // Cambiar icono
        const icon = this.querySelector('i');
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
    });
    
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
    
    // Funciones de ayuda
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
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
    
    function showSuccessMessage() {
        // Crear elemento de mensaje de éxito
        const successMsg = document.createElement('div');
        successMsg.className = 'success-message';
        successMsg.innerHTML = `
            <div class="success-content">
                <i class="fas fa-check-circle"></i>
                <p>¡Inicio de sesión exitoso!</p>
            </div>
        `;
        
        // Estilos dinámicos
        successMsg.style.position = 'fixed';
        successMsg.style.top = '0';
        successMsg.style.left = '0';
        successMsg.style.width = '100%';
        successMsg.style.height = '100%';
        successMsg.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        successMsg.style.display = 'flex';
        successMsg.style.justifyContent = 'center';
        successMsg.style.alignItems = 'center';
        successMsg.style.zIndex = '1000';
        successMsg.style.animation = 'fadeIn 0.3s';
        
        // Estilos del contenido
        const successContent = successMsg.querySelector('.success-content');
        successContent.style.textAlign = 'center';
        successContent.style.color = 'white';
        successContent.style.padding = '30px';
        successContent.style.borderRadius = '10px';
        successContent.style.backgroundColor = 'rgba(39, 174, 96, 0.9)';
        successContent.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.3)';
        
        // Icono
        const icon = successMsg.querySelector('i');
        icon.style.fontSize = '50px';
        icon.style.marginBottom = '20px';
        icon.style.display = 'block';
        icon.style.color = 'white';
        
        // Agregar al documento
        document.body.appendChild(successMsg);
        
        // Redirigir después de 2 segundos (simulación)
        setTimeout(() => {
            // window.location.href = 'dashboard.html';
            successMsg.style.animation = 'fadeOut 0.3s';
            setTimeout(() => {
                successMsg.remove();
                loginForm.reset();
            }, 300);
        }, 2000);
    }
    
    // Agregar estilos de animación dinámicamente
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
    `;
    document.head.appendChild(style);
});