function is_valid_form (){
    let image_selected = document.getElementById('ambito-u');
    let option_colors = document.getElementsByName('color');
    let color_selected = false;


    for(let i = 0; i < option_colors.length; i++){
        if(option_colors[i].checked){
            color_selected = true;
        }
    }

    if (!color_selected){
        swal("Error", "Selecciona un color de fondo", "error");
        return false;
    }

    if (image_selected.value == null || image_selected.value == ""){
        swal("Error", "Selecciona una imagen", "error");
        return false;
    }
    let image_size= image_selected.files[0].size / 1024 / 1024;
    if (image_size > 10){
        swal("Error", "El archivo de seleccionado excede los 10 MB", "error");
        return false;
    }

}