function is_valid_form (){
    if($('#action').val() == "save"){
        let ambit_name = document.getElementById('id_name').value;
        if (ambit_name == '' || ambit_name == null){
            swal("Error", gettext('The name field is required'), "error");
            return false;
        }
        if(ambits_to_avoid.indexOf(ambit_name.toUpperCase()) != -1){
            swal("Error", gettext("This name is already taken"), "error");
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

        if (ambit_name == '' || ambit_name == null){
            swal("Error", gettext("The name field is required"), "error");
            return false;
        }

        if(!(is_published || space_free)){
            swal("Error", gettext("Delete an ambit before publish another"), "error");
            return false;
        }

        if(ambits_to_avoid.indexOf(ambit_name.toUpperCase()) != -1){
            swal("Error", gettext("This name is already taken"), "error");
            return false;
        }

        for(let i = 0; i < option_colors.length; i++){
            if(option_colors[i].checked){
                color_selected = true;
            }
        }

        if (!color_selected){
            swal("Error", gettext("Select a background color"), "error");
            return false;
        }


        if(image_selected.value != null && image_selected.value != ""){
            let image_size= image_selected.files[0].size / 1024 / 1024;
            if (image_size > 10){
                swal("Error", gettext("The size of the file must be less than 10 MB"), "error");
                return false;
            }

            let image_selected_regexp = new RegExp('/.png');
            let match_found = image_selected_source.search('.png');
            if (image_selected.value == null || image_selected.value == ""){
                swal("Error", gettext("Select a PNG image"), "error");
                return false;
            }
            if(match_found == -1){
                swal("Error", gettext("Select a PNG image"), "error");
                return false;
            }
        }


        return true;
    }


}

$(document).ready(function () {

    $(":submit").click(function () { $("#action").val(this.name); });
    for(let i=0; i<self_materias.length;i++){
        $("#sortable").append('<li class="ui-state-default"><span class="ui-icon ui-icon-arrowthick-2-n-s sorter"></span>' + self_materias[i] + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
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