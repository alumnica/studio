function is_valid_form (){
    var image_selected = document.getElementById('ambito-u').value;
    var option_colors = document.getElementsByName('color');
    var color_selected = false;

    for(var i = 0; i < option_colors.length; i++){
        if(option_colors[i].checked){
            color_selected = true;
        }
    }

    if (!color_selected){
        swal("Error", "Selecciona un color de fondo", "error");
        return false;
    }

    if (image_selected == null || image_selected == ""){
        swal("Error", "Selecciona una imágen", "error");
        return false;
    }

}