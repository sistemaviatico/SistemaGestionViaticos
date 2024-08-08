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



/*Viaticos*/
/*Registrar viaticos CHECKBOXS*/

document.addEventListener('DOMContentLoaded', () => {
    // Aquí va tu código JavaScript
//         const checkbox_Desayuno = document.getElementById('checkboxMontoDesayuno');
//         const input_Desayuno = document.getElementById('mostrarMontoDesayuno');

//         const checkbox_Almuerzo = document.getElementById('checkboxMontoAlmuerzo');
//         const input_Almuerzo = document.getElementById('mostrarMontoAlmuerzo');
        
//         const checkbox_Cena = document.getElementById('checkboxMontoCena');
//         const input_Cena = document.getElementById('mostrarMontoCena');

//         const checkbox_Hospedaje = document.getElementById('checkboxMontoHospedaje');
//         const input_Hospedaje = document.getElementById('mostrarMontoHospedaje');

//         const checkbox_Leon = document.getElementById('checkboxMontoLeon');
//         const input_Leon = document.getElementById('mostrarMontoLeon');

//         const checkbox_Managua = document.getElementById('checkboxMontoManagua');
//         const input_Managua = document.getElementById('mostrarMontoManagua');

//         const checkbox_Otros = document.getElementById('checkboxOtros');
//         const input_Otros = document.getElementById('mostrarMontoOtros');

        
//         checkbox_Desayuno.addEventListener('change', () => {
//             if (checkbox_Desayuno.checked) {
//                 input_Desayuno.value = '300.00';
//             } else {
//                 input_Desayuno.value = '0.00';
//             }
//         });
//         checkbox_Almuerzo.addEventListener('change', () => {
//             if (checkbox_Almuerzo.checked) {
//                 input_Almuerzo.value = '350.00';
//             } else {
//                 input_Almuerzo.value = '0.00';
//             }
//         });
//         checkbox_Cena.addEventListener('change', () => {
//             if (checkbox_Cena.checked) {
//                 input_Cena.value = '300.00';
//             } else {
//                 input_Cena.value = '0.00';
//             }
//         });
//         checkbox_Hospedaje.addEventListener('change', () => {
//             if (checkbox_Hospedaje.checked) {
//                 input_Hospedaje.value = '500.00';
//             } else {
//                 input_Hospedaje.value = '0.00';
//             }
//         });
//         checkbox_Leon.addEventListener('change', () => {
//             if (checkbox_Leon.checked) {
//                 input_Leon.value = '200.00';
//             } else {
//                 input_Leon.value = '0.00';
//             }
//         });
//         checkbox_Managua.addEventListener('change', () => {
//             if (checkbox_Managua.checked) {
//                 input_Managua.value = '350.00';
//             } else {
//                 input_Managua.value = '0.00';
//             }
//         });
//         checkbox_Otros.addEventListener('change', () => {
//             if (checkbox_Otros.checked) {
//                 input_Otros.value = '200.00';
//             } else {
//                 input_Otros.value = '0.00';
//             }
//         });
  
//     // ... resto del código
const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const totalInput = document.getElementById('mostrarMontoCordobas');
    const totalInputDolaes = document.getElementById('mostrarMontoDolares')

    function handleCheckboxChange(event) {
        const checkbox = event.target;
        const input = checkbox.previousElementSibling;
        const monto = parseFloat(checkbox.dataset.monto);

        if (checkbox.checked) {
            input.value = monto.toFixed(2);
        } else {
            input.value = "0.00";
        }

        actualizarTotal();
    }

    function actualizarTotal() {
        let total = 0;
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                total += parseFloat(checkbox.dataset.monto);
            }
        });
        dolares = total.toFixed(2) / 36.80
        totalInput.value = total.toFixed(2);
        totalInputDolaes.value = dolares.toFixed(2)
    }

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', handleCheckboxChange);
    });
    
    // imprimir
    printButton.addEventListener('click', function() {
        const printContents = document.querySelector('.informacion-viatico').innerHTML;
        const originalContents = document.body.innerHTML;

        document.body.innerHTML = `<div>${printContents}</div>`;

        window.print();

        document.body.innerHTML = originalContents;
        window.location.block(); // Recargar la página para restaurar los eventos de los botones
    });
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
