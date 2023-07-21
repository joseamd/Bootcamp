
// <!--modalGestion-->
	var $ = jQuery.noConflict();    
	function abrir_modal_gestion(url,id_bootcamp){
		$("#modalGestion").load(url, function(){ 
            document.getElementById('id_bootcamp').value=id_bootcamp;            
			$(this).modal('show');
		});
	};

	var $ = jQuery.noConflict();    
	function abrir_modal_notificacion(url,mensaje){
		$("#modalGestion").load(url, function(){ 
            document.getElementById('mensaje').value=mensaje;
			$(this).modal('show');
		});
	};


// <!--Seleccion_estudiante.html Tabla Seleccion_estudiantes-->
    $(document).on('submit','#task-form',function(e){
        e.preventDefault();
        var formData = $('#task-form').serialize();
        $.ajax({
            type:$('#task-form').attr('method'),
            url:$('#task-form').attr('action'),
            data: formData,
            success: function(response) {                
                Swal.fire({
                    icon: 'success',
                    title: 'Lista de Aprobados',
                    text: 'Actualizada correctamente!',
                    confirmButtonColor: '#2d353c',
                })     
            }            
         
        })
        $('#modalGestion').modal('hide');
    });


    
// <!--CONTENIDO-notificacion.html Tabla Participantes-->  
    $(document).on('submit','#form_notificacion',function(e){
        e.preventDefault();
        var formData = $('#form_notificacion').serialize();
        $.ajax({
            type:$('#form_notificacion').attr('method'),
            url:$('#form_notificacion').attr('action'),
            data: formData,
            success: function(response) {                
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje',
                    text: 'Enviado satisfactoriamente',
                    confirmButtonColor: '#2d353c',
                })     
            }         
        })
        $('#modalGestion').modal('hide');
    });


    // Data-table multiplex

    $('table.display').DataTable({
        "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
        },
        responsive: true,
        dom: '<"dataTables_wrapper dt-bootstrap"<"row"<"col-xl-7 d-block d-sm-flex d-xl-block justify-content-center"<"d-block d-lg-inline-flex me-0 me-md-3"l><"d-block d-lg-inline-flex"B>><"col-xl-5 d-flex d-xl-block justify-content-center"fr>>t<"row"<"col-md-5"i><"col-md-7"p>>>',
        buttons: [
        { extend: 'copy', className: 'btn-sm' },
        { extend: 'csv', className: 'btn-sm' },
        { extend: 'excel', className: 'btn-sm' },
        { extend: 'pdf', className: 'btn-sm' },
        { extend: 'print', className: 'btn-sm' }
        ],
        responsive: true,
        colReorder: true,
        keys: true,
        rowReorder: true,
        select: true
                });                  
    if ($(window).width() <= 767) {
        options.rowReorder = false;
        options.colReorder = false;
    };
    $("#id_datepicker-default").keyup(function(){
        table.column($(this).data('index')).search(this.value).draw();
    });            


        
    // CARGAMOS EL INPUT CON LA FECHA ACTUAL
    var hoy = new Date();
    var dia = hoy.getDate();
    var mes = hoy.getMonth() +1;
    var agnio = hoy.getFullYear();
   
    dia = ('0' + dia).slice(-2)
    mes = ('0' + mes).slice(-2)

    var agnio = date.toLocaleString("default", { year: "numeric" })
    var mes = date.toLocaleString("default", { month: "2-digit" })
    var dia = date.toLocaleString("default", { day: "2-digit" })
    var dateFormat = getDay + "-" + getMonth + "-" + getYear
    
    $(document).ready(function() {
        $("#id_datepicker-default").datepicker({
            todayHighlight: true,
            autoclose: true,
        }).datepicker("inputDate", dateFormat);
    });



    



    


    

  




