/**
 * Sets initial momentos data in case it exists for each microoda
 */
$(document).ready(function () {

    $("input[id='evaluation_file']").change(function (e) {
        var $this = $(this);
       $('#uoda-6').html($this.val().split('\\').pop());
    });

    $('#materia-a-oda').change(function () {
       subject_name = this.value;

       subject = subject_bloques.filter(x => x.name === subject_name);
       bloques = subject[0].bloques;
       select_bloques = $('#bloque-a-oda');
       select_bloques.empty();
       for(let i=0; i<bloques.length; i++){
           option = $('<option></option>').attr("value", bloques[i]).text(bloques[i]);
           select_bloques.append(option);
       }
   });

    $(":submit").click(function () {
    $("#action").val(this.name);
     });

     $('#materia-a-oda').val(self_subject);
     $('#materia-a-oda').trigger('change');

     $('#bloque-a-oda').val(self_section);

     for (let i=0; i<apli.length; i++){
        let text = apli[i].name;
        let value = apli[i].code;
        let url = '/momentos/select/'+value;


        $('#apli ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+url+'"></i>'  + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#apli ul').sortable('refresh');
        if ($('#apli ul li').length > 4) {
            $('#apli .add-materia').hide();
        }
    }

    for (let i=0; i<forma.length; i++){
        let text = forma[i].name;
        let value = forma[i].code;
        let url = '/momentos/select/'+value;

        $('#forma ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+url+'"></i>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#forma ul').sortable('refresh');
        if ($('#forma ul li').length > 4) {
            $('#forma .add-materia').hide();
        }
    }

    for (let i=0; i<activa.length; i++){
        let text = activa[i].name;
        let value = activa[i].code;
        let url = '/momentos/select/'+value;

        $('#activ ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+url+'"></i>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#activ ul').sortable('refresh');
        if ($('#activ ul li').length > 4) {
            $('#activ .add-materia').hide();
        }
    }
    for (let i=0; i<ejem.length; i++){
        let text = ejem[i].name;
        let value = ejem[i].code;
        let url = '/momentos/select/'+value;

        $('#ejemp ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+url+'"></i>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#ejemp ul').sortable('refresh');
        if ($('#ejemp ul li').length > 4) {
            $('#ejemp .add-materia').hide();
        }
    }

    for (let i=0; i<sens.length; i++){
        let text = sens[i].name;
        let value = sens[i].code;
        let url = '/momentos/select/'+value;

        $('#sens ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+url+'"></i>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#sens ul').sortable('refresh');
        if ($('#sens ul li').length > 4) {
            $('#sens .add-materia').hide();
        }
    }

   /* for (let i=0; i<evalu.length; i++){
        let text = evalu[i].name;
        let value = evalu[i].code;

        $('#eval ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+value+'"></i>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#eval ul').sortable('refresh');
        if ($('#eval ul li').length >= 1) {
            $('#eval .add-materia').hide();
        }*/
        if (evalu != null && evalu != ""){
            var dloadFile;
            var theUrl = '/api/evaluations/'+evalu.pk;
            $.ajax({
                url: theUrl,
                dataType: 'json',
                success: function(data) {
                dloadFile = data.file;
                $('#eval-dload').attr('href', dloadFile);
                }
            });
        }



});

/**
 * Validates at least one object has been positioned in a dropzone to retreives its zone number
 * @returns {boolean}
 */
function is_valid_form_position (){
    let position_inputs = document.getElementById('oda-position');

    if(position_inputs.value == "" || position_inputs.value == null){
        swal("Error", "Coloca al menos una oda en el bloque para guardar", "error");
        return false;
    }

    return true;

}

/**
 * Checks required fields depending on action
 * The action can be save or finalize.
 * Saving action only requires title
 * Finalize requieres all fields filled and at least one momento assigned to each microoda
 * @returns {boolean}
 */
function is_valid_form_odas_section(){

    if($('#action').val() == "save"){
        return true;
    }
    else{
        //tags
        let tags = document.getElementById('oda-tags').value;
        if (tags == '' || tags == null){
            swal("Error", "Introduce al menos un tag", "error");
            return  false;
        }

        //subject
        let subject = document.getElementById('materia-a-oda').value;
        if (subject == '' || subject == null){
            swal("Error", "Selecciona una materia", "error");
            return  false;
        }

        //section
        let bloque = document.getElementById('bloque-a-oda').value;
        if (bloque == '' || bloque == null){
            swal("Error", "Selecciona un bloque", "error");
            return  false;
        }

        //images
        let inputs = $("input.image:file");
        for (let i=0; i<inputs.length; i++) {
            if (!$(inputs[i]).parents('.my_item').hasClass('is-hidden')){
                if (inputs[i].files.length > 0) {
                let image_size = inputs[i].files[0].size / 1024 / 1024;
                if (image_size > 10) {
                    swal("Error", "El archivo seleccionado excede los 10 MB", "error");
                    return false;
                }
                else {
                preview_name = 'preview-' + inputs[i].name;
                let source_image = document.getElementById(preview_name).src;
                let match_png_found = source_image.search('data:image/png');
                let match_gif_found = source_image.search('data:image/gif');

                if(match_png_found == -1 &&  match_gif_found == -1){
                    swal("Error", "Debes subir archivos png o gif", "error");
                    return  false;
                }
            }
            }
            else {
                preview_name = 'preview-' + inputs[i].name;
                let source_image = document.getElementById(preview_name).src;
                let match_found = source_image.search('.png');

                if (source_image == "" || source_image == null) {
                    swal("Error", "Faltan imágenes por subir", "error");
                    return false;
                }

                let match_png_found = source_image.search('data:image/png');
                let match_gif_found = source_image.search('data:image/gif');
                if(match_png_found == -1 &&  match_gif_found == -1){
                    swal("Error", "Faltan imágenes por subir", "error");
                    return false;
                }
            }
            }


        }


        //microodas
        let aplicacion = document.getElementById('apli-momentos').value;
        if (aplicacion == '' || aplicacion == null){
            swal("Error", "Selecciona al menos un momento para la microoda Aplicación", "error");
            return  false;
        }

        let aplicacion_tags = document.getElementById('apli-tags').value;
        if (aplicacion_tags == '' || aplicacion_tags == null){
            swal("Error", "Escribe al menos un tag para la microoda Aplicación", "error");
            return  false;
        }

        let formalizacion = document.getElementById('forma-momentos').value;
        if (formalizacion == '' || formalizacion == null){
            swal("Error", "Selecciona al menos un momento para la microoda Formalización", "error");
            return  false;
        }
        let formalizacion_tags = document.getElementById('forma-tags').value;
        if (formalizacion_tags == '' || formalizacion_tags == null){
            swal("Error", "Escribe al menos un tag para la microoda Formalización", "error");
            return  false;
        }

        let activacion = document.getElementById('activ-momentos').value;
        if (activacion == '' || activacion == null){
            swal("Error", "Selecciona al menos un momento para la microoda Activación", "error");
            return  false;
        }
        let activacion_tags = document.getElementById('activ-tags').value;
        if (activacion_tags == '' || activacion_tags == null){
            swal("Error", "Escribe al menos un tag para la microoda Activación", "error");
            return  false;
        }

        let ejemplificacion = document.getElementById('ejem-momentos').value;
        if (ejemplificacion == '' || ejemplificacion == null){
            swal("Error", "Selecciona al menos un momento para la microoda Ejemplificación", "error");
            return  false;
        }
        let ejemplificacion_tags = document.getElementById('ejemp-tags').value;
        if (ejemplificacion_tags == '' || ejemplificacion_tags == null){
            swal("Error", "Escribe al menos un tag para la microoda Ejemplificación", "error");
            return  false;
        }

        let sensibilizacion = document.getElementById('sens-momentos').value;
        if (sensibilizacion == '' || sensibilizacion == null){
            swal("Error", "Selecciona al menos un momento para la microoda Sensibilización", "error");
            return  false;
        }
        let sensibilizacion_tags = document.getElementById('sens-tags').value;
        if (sensibilizacion_tags == '' || sensibilizacion_tags == null){
            swal("Error", "Escribe al menos un tag para la microoda Sensibilización", "error");
            return  false;
        }

        let evaluacion = document.getElementById('evaluation_file');
        if (evaluacion.files.length > 0) {
            let evaluacion_size = evaluacion.files[0].size / 1024 / 1024;
                if (evaluacion_size > 10) {
                    swal("Error", "El archivo de seleccionado excede los 10 MB", "error");
                    return false;
                }
        }
        else{
            let evaluation_object = document.getElementById('eval-momentos').value;
            if (evaluation_object == "" || evaluation_object == null){
                let evaluation_file = document.getElementById('uoda-6').innerText;
                if(evaluation_file == "" || evaluation_file == null){
                    swal("Error", "Selecciona una evaluación", "error");
                    return  false;
                }
            }

        }
        return true;
    }




}
