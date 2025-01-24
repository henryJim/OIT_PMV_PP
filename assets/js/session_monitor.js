// Verificar si el usuario está autenticado
fetch('/api/check-auth/')
    .then(response => response.json())
    .then(data => {
        var userLoggedIn = data.isAuthenticated;
        console.log(userLoggedIn ? "Usuario autenticado" : "Usuario no autenticado");

        // Si el usuario está autenticado, crear el WebSocket
        if (userLoggedIn) {
            console.log("Usuario autenticado, creando WebSocket...");
            createSocket();
        } else {
            console.log("El usuario no está autenticado, no se crea el WebSocket.");
        }
    })
    .catch(error => {
        console.error('Error al verificar autenticación', error);
    });

let socket;
let sessionExpired = false;

function createSocket() {
    console.log("Creando WebSocket...");
    socket = new WebSocket('ws://164.90.138.17:8001/ws/session_expiration/');

    socket.onopen = function(event) {
        console.log('WebSocket está abierto, podemos enviar mensajes.');

        // Ahora que la conexión está abierta, puedes iniciar la verificación de la sesión
        setInterval(function () {
            if (socket && socket.readyState === WebSocket.OPEN) { // Verificación adicional
                console.log("Enviando solicitud para verificar la sesión...");
                socket.send(JSON.stringify({ check_session: true }));
            }
        }, 60000);
    };

    socket.onmessage = function(event) {
        let message = JSON.parse(event.data);
        console.log('Mensaje recibido:', message);

        if (message.status === 'session_expired' && !sessionExpired) {
            socket.close();

            // Mostrar la alerta solo una vez
            Swal.fire({
                title: "Sesión Expirada",
                text: "Tu sesión ha expirado. Serás redirigido al login.",
                icon: "warning"
            }).then(function() {
                // Cerrar el WebSocket antes de redirigir
                // Redirigir después de que el usuario cierre la alerta
                window.location.href = '/signin/';
            });
            sessionExpired = true;  // Establecer la bandera para evitar que se muestre la alerta nuevamente
        } else if (message.status === 'session_active') {
            console.log('La sesión sigue activa');
            sessionExpired = false;  // Restablecer la bandera si la sesión está activa
        } else if (message.status === 'session_inactive') {
            console.log('El usuario no está autenticado');
        }
    };

    socket.onerror = function(event) {
        console.error('Error en WebSocket:', event);
    };

    socket.onclose = function(event) {
        console.log('WebSocket cerrado:', event);
        socket = null; // Elimina la referencia del socket cuando se cierre
    };
}
