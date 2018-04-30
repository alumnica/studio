function is_valid_form (){
    let image_selected = document.getElementById('ambito-u');
    let option_colors = document.getElementsByName('color');
    let color_selected = false;
    let image_selected_source = document.getElementById('preview-ap').src;
    let ambit_name = document.getElementById('id_name_field').value;

    if(ambits_to_avoid.indexOf(ambit_name.toUpperCase()) != -1){
        swal("Error", "Este nombre ya está siendo usado por otro ámbito", "error");
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

    if ((image_selected.value == null || image_selected.value == "") && image_selected_source == null  && image_selected_source == ""){
        swal("Error", "Selecciona una imagen", "error");
        return false;
    }

    if(image_selected.value != null && image_selected.value != ""){
        let image_size= image_selected.files[0].size / 1024 / 1024;
        if (image_size > 10){
            swal("Error", "El archivo de seleccionado excede los 10 MB", "error");
            return false;
        }
    }


    return true;

}

$(document).ready(function () {

    for(let i=0; i<self_materias.length;i++){
        $("#sortable").append('<li class="ui-state-default"><span class="ui-icon ui-icon-arrowthick-2-n-s sorter"></span>' + self_materias[i] + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $("#sortable").sortable('refresh');
        if ($('ul#sortable li').length > 3) {
            $('#add-materia-button').hide();
        }
    }
    if (self_color!= null && self_color!=""){
        radio_btn = document.getElementById(self_color);
        radio_btn.checked = true;
        $(radio_btn).trigger('click');
    }

});