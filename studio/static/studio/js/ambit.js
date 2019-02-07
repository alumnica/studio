/**
 * Adds color radio buttons click functionality and retrieves assigned subjects list
 */
$(document).ready(function () {

    $(":submit").on('click', function () {

        let texts = [];

        $('#sortable li').each(function () {
            let currentLi = $(this);

            texts.push(currentLi.text());
        });
        $('#class_name').val(texts.join('|'));

        $("#action").val(this.name);
    });



    for(let i=0; i<self_materias.length;i++){
        $("#sortable").append('<li class="ui-state-default"><span class="ui-icon ui-icon-arrowthick-2-n-s sorter"></span>' + self_materias[i].name + '</a><span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $("#sortable").sortable('refresh');
        if ($('ul#sortable li').length > 3) {
            $('#add-materia-button').hide();
        }
    }
    if (self_color!= null && self_color!="" && self_color != 'None'){
        radio_btn = document.getElementById(self_color);
        radio_btn.checked = true;
        $(radio_btn).trigger('click');
    }

});

/**
 * Reviews required fields depending on the action
 * Action can be save or finalize. All fields are required for finalize action
 * @returns {boolean} True if all the action required fields are given
 */
function is_valid_ambit_form (){
        if($('#action').val() == "save"){
            let ambit_name = document.getElementById('id_name').value;
            if (ambit_name == '' || ambit_name == null){
                swal("Error", 'Escribe el nombre para continuar', "error");
                return false;
            }
            if(ambits_to_avoid.indexOf(ambit_name.toUpperCase()) != -1){
                swal("Error", "Este nombre ya está siendo usado", "error");
                return false;
            }
            return true;
        }
        else{
            let image_selected = document.getElementById('ambito-u');
            let option_colors = document.getElementsByName('color');
            let color_selected = false;
            let image_selected_source = document.getElementById('preview-ap').src;
            let ambit_name = document.getElementById('id_name').value;
            let subjects_selected = document.getElementById('class_name').value;

            let first_badge = document.getElementById('aUpload');
            let first_badge_source = document.getElementById('preview-aU').src;
            let second_badge = document.getElementById('bUpload');
            let second_badge_source = document.getElementById('preview-bU').src;
            let third_badge = document.getElementById('cUpload');
            let third_badge_source = document.getElementById('preview-cU').src;

            if (ambit_name == '' || ambit_name == null){
                swal("Error", 'El campo de nombre es requerido', "error");
                return false;
            }

            if(!(is_published || space_free)){
                swal("Error", "Elimina uno de los Ámbitos antes de crear uno nuevo", "error");
                return false;
            }

            if(ambits_to_avoid.indexOf(ambit_name.toUpperCase()) != -1){
                swal("Error", "Este nombre ya está siendo usado", "error");
                return false;
            }

            for(let i = 0; i < option_colors.length; i++){
                if(option_colors[i].checked){
                    color_selected = true;
                }
            }

            if (!color_selected){
                swal("Error", "Selecciona un color de fondo", "error");
                return false;
            }


            if(image_selected.value != null && image_selected.value != ""){
                let image_size= image_selected.files[0].size / 1024 / 1024;
                if (image_size > 10){
                    swal("Error", "El archivo seleccionado excede los 10 MB", "error");
                    return false;
                }

                let image_selected_regexp = new RegExp('/.png');
                let match_found = image_selected_source.search('image/png');
                if(match_found == -1){
                    swal("Error", "Selecciona una imagen PNG", "error");
                    return false;
                }
            }
            else{
                let match_found = image_selected_source.search('.png');
                if(match_found == -1){
                    swal("Error", "Selecciona una imagen PNG", "error");
                    return false;
                }
            }


            if(first_badge.value != null && first_badge.value != ""){
                let image_size= first_badge.files[0].size / 1024 / 1024;
                if (image_size > 10){
                    swal("Error", "El archivo seleccionado para la primera versión de la insignia excede los 10 MB", "error");
                    return false;
                }

                let match_found = first_badge_source.search('image/png');
                if(match_found == -1){
                    swal("Error", "Selecciona una imagen PNG para la primera versión de la insignia", "error");
                    return false;
                }
            }
            else{
                let match_found = first_badge_source.search('.png');
                if(match_found == -1){
                    swal("Error", "Selecciona una imagen PNG para la primera versión de la insignia", "error");
                    return false;
                }
            }


            if(second_badge.value != null && second_badge.value != ""){
                let image_size= first_badge.files[0].size / 1024 / 1024;
                if (image_size > 10){
                    swal("Error", "El archivo seleccionado para la segunda versión de la insignia excede los 10 MB", "error");
                    return false;
                }

                let match_found = second_badge_source.search('image/png');
                if(match_found == -1){
                    swal("Error", "Selecciona una imagen PNG para la segunda versión de la insignia", "error");
                    return false;
                }
            }
            else{
                let match_found = second_badge_source.search('.png');
                if(match_found == -1){
                    swal("Error", "Selecciona una imagen PNG para la segunda versión de la insignia", "error");
                    return false;
                }
            }


            if(third_badge.value != null && third_badge.value != ""){
                let image_size= first_badge.files[0].size / 1024 / 1024;
                if (image_size > 10){
                    swal("Error", "El archivo seleccionado para la tercera versión de la insignia excede los 10 MB", "error");
                    return false;
                }

                let match_found = third_badge_source.search('image/png');
                if(match_found == -1){
                    swal("Error", "Selecciona una imagen PNG para la tercera versión de la insignia", "error");
                    return false;
                }
            }
            else{
                let match_found = third_badge_source.search('.png');
                if(match_found == -1){
                    swal("Error", "Selecciona una imagen PNG para la tercera versión de la insignia", "error");
                    return false;
                }
            }


            if (subjects_selected == '' || subjects_selected == null){
                swal("Error", "Asigna al menos una materia para publicar", "error");
                return false;
            }

            return true;
        }


    }