$(document).ready(function(){
    $('#tablaPerfiles').on('click', '.perfil_info_btn', function() {
        let perfilId = $(this);
        let id_p = perfilId.attr('value');
        console.log(id_p)
        obtener_info(id_p);
        
    })
    function obtener_info(id) {
        console.log(id)
        $.get(`/obtener_info/${id}`, function(data) {
            if (!data.error) {
                $('#nuevo_perfil').val(data.perfil);
                $('#id_perfil').val(data.perfilid);
            } else {
                alert('Error: ' + data.error);
            }
        });
    }

});


/*Abrir modal de perfiles*/
function abrirModalPerfil(){
    document.getElementById('myModalPerfil').style.display = 'block';
    document.getElementById('modalOverlay').style.display = 'block';
}
/*Cerrar modal de perfiles*/
function cerrarModalPerfil(){
    document.getElementById('myModalPerfil').style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
}
