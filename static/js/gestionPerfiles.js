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

/*gestionPersonal*/
function buscarNumeroEmpleado() {
    var select = document.getElementById("nombresEmpleadoSelect");
    var empleadoId = select.value;

    fetch(`/get_numero_empleado/${empleadoId}`)
        .then(response => response.json())
        .then(data => {
            // document.getElementById("mostrarNumeroEmpleado").value = data.numeroEmpleado;
            document.getElementById("MostrarNumeroEmpleado").value = data.numeroEmpleado;
            document.getElementById("mostrarNombresEmpleado").value = data.nombresEmpleado;
            document.getElementById("mostrarDepatamento").value = data.departamento;
            document.getElementById("mostrarArea").value = data.area;
            document.getElementById("mostrarCecc").value = data.cecc;
            document.getElementById("mostrarCedula").value = data.cedula;

        })
        .catch(error => console.error('Error:', error));
} 






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
