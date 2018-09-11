$(document).ready(function () {
    let fnum = $('.my_item').length;
    fnum = fnum - 1;
    if(fnum>0){
        let theItem = $('.my_item')[fnum]
        $(theItem).find('.delete').show();
    }

    $(":submit").click(function () { $("#action").val(this.name); });
    // Code adapted from http://djangosnippets.org/snippets/1389/
    let x = 0;

    function updateElementIndex(el, prefix, ndx) {
        let id_regex = new RegExp('(' + prefix + '-\\d+-)');
        let replacement = prefix + '-' + ndx + '-';
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
        replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    /**
     * Hides selected form and turns on the delete attribute
     * @param btn
     * @param prefix
     * @returns {boolean}
     */
    function deleteForm(btn, prefix) {
        let formCount = 0;

        $(".my_item").each(function () {
           if (this.className.search('is-hidden') == -1){
               formCount += 1;
           }
        });

        if (formCount > 1) {
//            let row = $(".my_item:first").clone(false).get(0);
            // Delete the item/form
            id_name = $(btn).parents('.my_item').find('.upload_section').attr('id');

            number_form= id_name.split('-')[1];
            $('#form-'+ number_form+ '-DELETE').val('on');
            $(btn).parents('.my_item').addClass('is-hidden');
//            $(btn).parents('.my_item').find('.delete').removeAttr('style');
            let numForm = number_form - 1;
            if (numForm >= 1){
               $('#id_form-'+numForm+'-file').parents('.my_item').find('.delete').show()

            }
            let forms = $('.my_item'); // Get all the forms
            // Update the total number of forms (1 less than before)
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            // Go through the forms and set their indices, names and IDs
            // let label_name = document.getElementsByClassName('section_name');
            // for (index = 0; index < label_name.length; ++index) {
            //     label_name[index].innerText = ("Bloque # " + (index + 1));
            // }

            let counter = 1;
             $(".my_item").each(function () {
                if(this.className.search('is-hidden') == -1){
                    let label_name = $(this).find('.section_name');
                    $(label_name).text( "Bloque # " + (counter));
                    counter += 1;
                }
            });

                if (formCount == 4) {
                    $('#bloque-add').show();
            }
        }// End if
        else {
            swal("Error", "Debe existir al menos un bloque!", "error");
        }
        return false;
    }

    /**
     * Assigns target attribute to each image input
     * @param input
     */
    function readURL(input) {
        if (input.files && input.files[0]) {
            let reader = new FileReader();

            reader.onload = function (e) {
                let cosa = '#preview-' + $(input).attr('name');
                $(cosa).attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    }

    /**
     * Adds form to formset if the not hidden forms count is less than 4, cloning the first form.
     * While creating new form, it assigns names and form numbers
     * @param btn Button clicked
     * @param prefix Form prefix
     * @returns {boolean}
     */
    function addForm(btn, prefix) {
        let formCount = 0;
        let hiddenForms = 0;

        $(".my_item").each(function () {
           if (this.className.search('is-hidden') == -1){
               formCount += 1;
           }
           else{
               hiddenForms += 1;
           }
        });
        if(hiddenForms > 0){
            let one_shown = false;
            $(".my_item").each(function () {
           if (this.className.search('is-hidden') != -1 && !one_shown){
               $(this).removeClass('is-hidden');
               $(this).find('.img-preview').removeAttr('src');
               $(this).find('.upload_section').val('');

            $('#id_form-'+(formCount-1)+'-file').parents('.my_item').find('.delete').hide();
               $(this).find('.delete').show();

               id_name = $(this).find('.upload_section').attr('id');
               number_form= id_name.split('-')[1];
               $('#form-'+ number_form+ '-DELETE').removeAttr('value');
               one_shown = true;
           }
        });
        }
        else{
             // You can only submit a maximum of 10 todo items
        if (formCount < 4) {
            // Clone a form (without event handlers) from the first form
            let row = "";
            $(".my_item").each(function () {
                if(this.className.search('is-hidden') == -1){
                    row = $(this).clone(false).get(0);
                }
            });
            $('#id_form-'+(formCount-1)+'-file').parents('.my_item').find('.delete').hide();
            let inputs = row.getElementsByTagName('input');
            for (index = 0; index < inputs.length; ++index) {
                updateElementIndex(inputs[index], prefix, formCount);
                $(inputs[index]).val("");
                 if ($(inputs[index]).is( "[type=file]" ) ) {
                    $(inputs[index]).change(function () {
                        readURL(this);
                    });
        }
            }
            let position_btn = row.getElementsByTagName('button');
            for (index = 0; index < position_btn.length; ++index) {
                let name = $(position_btn[index]).attr('name');
                if (name != '' && name!=null && typeof name !== typeof undefined){
                     $(position_btn[index]).attr('name','position-form-'+formCount);
                }
            }


            let labels = row.getElementsByTagName('label');
            for (index = 0; index < labels.length; ++index) {
                updateElementIndex(labels[index], prefix, formCount);
            }

            let label_name = row.getElementsByTagName('span')[0];
            label_name.innerText = ("Bloque # " + (formCount + 1));


            let images = row.getElementsByTagName('img');
            for (index = 0; index < images.length; ++index) {
                updateElementIndex(images[index], prefix, formCount);
                $(images[index]).removeAttr('src')
            }


            // Insert it after the last form
            $(row).removeAttr('id').hide().insertAfter(".my_item:last").slideDown(100);

            // Remove the bits we don't want in the new row/form
            // e.g. error messages
            $(".errorlist", row).remove();
            $(row).children().removeClass("error");
            // Relabel or rename all the relevant bits


            $(row).children().children().each(function () {
                updateElementIndex(this, prefix, formCount);
                $(this).val("");
            });

            // Add an event handler for the delete item/form link
            $(row).find(".delete").click(function () {



                return deleteForm(this, prefix);
            });
            // Update the total form count
            $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);
            $(":submit").click(function () { $("#action").val(this.name); });
            if(formCount==3){
                $('#bloque-add').hide();
            }
        } // End if
        else {
            swal("Error", "Sólo puedes añadir un máximo de 4 bloques", "error");
        }
        }

        return false;
    }
    // Register the click event handlers
    $("#add").on('click', function () {




        return addForm(this, "form");
    });

    $(".delete").on('click', function () {

        return deleteForm(this, "form");
    });
});

/**
 * Reviews all required fields before submit, depending on the action.
 * Action can be save, requiring only the title, or eva-publish, requiring all fields
 * @returns {boolean}
 */
function is_valid_form_subject(){
    if($('#action').val() != "eva-publish"){
        if($('#action').val() != "save"){
           let btn_name = $('#action').val();
           let btn = document.getElementsByName(btn_name);
           let img_preview = $(btn).parents('.my_item').find('.img-preview').attr('src');
           let match_png_found = img_preview.search('.png');
           let match_jpg_found = img_preview.search('.jpg');
           let match_jpeg_found = img_preview.search('.jpeg');

                if (img_preview == "" || source_image == null) {
                    swal("Error", "Sube una imagen antes de editar las posiciones", "error");
                    return false;
                }

                if(match_png_found == -1 && match_jpg_found == -1 && match_jpeg_found == -1){
                    swal("Error", "Sube una imagen antes de editar las posiciones", "error");
                    return false;
                }

        }
        return true;
    }
    else{
        let ambit_selected = document.getElementById('id_ambit').value;
        let tags = document.getElementById('materias-tags').value;

        if (tags == '' || tags==' ' || tags ==null){
            swal("Error", "Debes introducir al menos un tag para finalizar", "error");
            return false;
        }

        if (ambit_selected == '' || ambit_selected ==null){
            swal("Error", "Debes seleccionar un ámbito para finalizar", "error");
            return false;
        }


        let inputs = $("form input[type='file']");
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
                let source_image = (document.getElementById(preview_name)).getAttribute('src');
                let match_png_found = source_image.search('.png');
                let match_jpg_found = source_image.search('.jpg');
                let match_jpeg_found = source_image.search('.jpeg');

                if(match_png_found == -1 && match_jpg_found == -1 && match_jpeg_found == -1){
                    swal("Error", "Debes subir archivos png, jpg o jpeg", "error");
                    return false;

                }
            }
            }
            else {
                preview_name = 'preview-' + inputs[i].name;
                let source_image = (document.getElementById(preview_name)).getAttribute('src');

                if (source_image == "" || source_image == null) {
                    swal("Error", "Faltan imágenes por subir", "error");
                    return false;
                }

                let match_png_found = source_image.search('.png');
                let match_jpg_found = source_image.search('.jpg');
                let match_jpeg_found = source_image.search('.jpeg');

                if(match_png_found == -1 && match_jpg_found == -1 && match_jpeg_found == -1){
                    swal("Error", "Debes subir archivos png, jpg o jpeg", "error");
                    return false;

                }
            }
            }


        }



        return true;
    }
}