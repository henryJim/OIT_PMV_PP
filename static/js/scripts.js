$(document).ready(function() {
    new DataTable('#tasks');
    new DataTable('#instructores', {
        language: {
            url: '//cdn.datatables.net/plug-ins/2.1.8/i18n/es-ES.json',
        }
    });
    new DataTable('#aprendices', {
        language: {
            url: '//cdn.datatables.net/plug-ins/2.1.8/i18n/es-ES.json',
        }
    });
});
