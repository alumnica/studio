$(document).ready(function () {

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

    $(":submit").click(function () { $("#action").val(this.name); });
     $('#materia-a-oda').val(self_subject);
     $('#materia-a-oda').trigger('change');

     $('#bloque-a-oda').val(self_section);



});


function is_valid_form_position (){
    let position_inputs = document.getElementsByTagName('input');

    for(let i = 0; i < position_inputs.length; i++){
        if(position_inputs[i].value == "" || position_inputs[i].value == null){
            swal("Error", "Coloca todas las ODAs en la imagen de sección", "error");
            return false;
        }
    }
    return true;

}

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
        let inputs = $("form input[type='file']");
        for (let i=0; i<inputs.length; i++) {
            if (!$(inputs[i]).parents('.my_item').hasClass('is-hidden')){
                if (inputs[i].files.length > 0) {
                let image_size = inputs[i].files[0].size / 1024 / 1024;
                if (image_size > 10) {
                    swal("Error", "El archivo de seleccionado excede los 10 MB", "error");
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

                let match_png_found = source_image.search('.png');
                let match_gif_found = source_image.search('.gif');
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

        let formalizacion = document.getElementById('forma-momentos').value;
        if (formalizacion == '' || formalizacion == null){
            swal("Error", "Selecciona al menos un momento para la microoda Formalización", "error");
            return  false;
        }

        let activacion = document.getElementById('activ-momentos').value;
        if (activacion == '' || activacion == null){
            swal("Error", "Selecciona al menos un momento para la microoda Activación", "error");
            return  false;
        }

        let ejemplificacion = document.getElementById('ejem-momentos').value;
        if (ejemplificacion == '' || ejemplificacion == null){
            swal("Error", "Selecciona al menos un momento para la microoda Ejemplificación", "error");
            return  false;
        }

        let sensibilizacion = document.getElementById('sens-momentos').value;
        if (sensibilizacion == '' || sensibilizacion == null){
            swal("Error", "Selecciona al menos un momento para la microoda Sensibilización", "error");
            return  false;
        }

        let evaluacion = document.getElementById('eval-momentos').value;
        if (evaluacion == '' || evaluacion == null){
            swal("Error", "Selecciona una evaluación", "error");
            return  false;
        }

    }




}
