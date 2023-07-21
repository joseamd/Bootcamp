// Funciones para eliminar registros

function borrar_clase_alert(id_clase,clase_name){
    Swal.fire({
        title: 'Estás seguro de eliminar el registro',
        text: ""+clase_name+"?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#2d353c',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, confirmo',
        cancelButtonText: 'Cancelar',
        }).then((result) => {
        if (result.isConfirmed) {									
            window.location.href = "/campus/delete_clase/"+id_clase+"/"					
        }
        })
    }
function borrar_notificacion(id_notificacion){
    Swal.fire({
        title: 'Estás seguro de eliminar el mensaje',
        text: "",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#2d353c',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, confirmo',
        cancelButtonText: 'Cancelar',
        }).then((result) => {
        if (result.isConfirmed) {									
            window.location.href = "/campus/delete_notificacion/"+id_notificacion+"/"					
        }
        })
    }
    function borrar_registro_alert(id_recurso,registro_name){
    Swal.fire({
        title: 'Estás seguro de eliminar el registro',
        text: ""+registro_name+"?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#2d353c',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, confirmo',
        cancelButtonText: 'Cancelar',
        }).then((result) => {
        if (result.isConfirmed) {									
            window.location.href = "/campus/delete_recurso/"+id_recurso+"/"					
        }
        })
    }
    function borrar_asignacion_alert(id_asignacion,registro_name){
    Swal.fire({
        title: 'Estás seguro de eliminar el registro',
        text: ""+registro_name+"?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#2d353c',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, confirmo',
        cancelButtonText: 'Cancelar',
        }).then((result) => {
        if (result.isConfirmed) {									
            window.location.href = "/campus/delete_asignacion/"+id_asignacion+"/"					
        }
        })
    }
    function borrar_entrega_alert(id_entrega){
    Swal.fire({
        title: 'Estás seguro de eliminar la entrega?',
        text: "",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#2d353c',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, confirmo',
        cancelButtonText: 'Cancelar',
        }).then((result) => {
        if (result.isConfirmed) {									
            window.location.href = "/campus/delete_entrega/"+id_entrega+"/"					
        }
        })
    }
    function borrar_evento(id_evento){
    Swal.fire({
        title: 'Estás seguro de eliminar el evento?',
        text: "",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#2d353c',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, confirmo',
        cancelButtonText: 'Cancelar',
        }).then((result) => {
        if (result.isConfirmed) {									
            window.location.href = "/campus/delete_evento/"+id_evento+"/"					
        }
        })
    }


