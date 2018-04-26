
$(document).ready(function () {
    // Code adapted from http://djangosnippets.org/snippets/1389/
    let x = 0;

$("input[type='text']").each(function(){
    $('#id_form-'+x+'-oda_name').selectize({
        maxItems: 1,
        labelField: 'name',
        valueField: 'name',
        searchField: 'name',
        hideSelected: true,
        persist: false,
        createOnBlur: true,
        create: function(input) {
            return {
                value: input,
                name: input
            }
        },
        options: odaList,
        preload: false,
        onInitialize: function(){
            let selectize = this;
            selectize.setValue(self_oda_selectize[x])
        }
    });
    x++;
});

    function updateElementIndex(el, prefix, ndx) {
        let id_regex = new RegExp('(' + prefix + '-\\d+-)');
        let replacement = prefix + '-' + ndx + '-';
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
        replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function deleteForm(btn, prefix) {
        let formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (formCount > 1) {
            // Delete the item/form
            $(btn).parents('.my_item').remove();
            let forms = $('.my_item'); // Get all the forms
            // Update the total number of forms (1 less than before)
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            // Go through the forms and set their indices, names and IDs
            let inputs = row.getElementsByTagName('input');
            for (index = 0; index < inputs.length; ++index) {
                updateElementIndex(inputs[index], prefix, formCount);
                $(inputs[index]).val("");
            }
            let labels = row.getElementsByTagName('label');
            for (index = 0; index < labels.length; ++index) {
                updateElementIndex(labels[index], prefix, formCount);
            }

            let images = row.getElementsByTagName('img');
            for (index = 0; index < images.length; ++index) {
                updateElementIndex(images[index], prefix, formCount);
                $(images[index]).removeAttr('src')
            }
        } // End if
        else {
            alert("You have to enter at least one item!");
        }
        return false;
    }

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

    function addForm(btn, prefix) {
        let formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        // You can only submit a maximum of 10 todo items
        if (formCount < 8) {
            // Clone a form (without event handlers) from the first form
            let row = $(".my_item:first").clone(false).get(0);

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
            let labels = row.getElementsByTagName('label');
            for (index = 0; index < labels.length; ++index) {
                updateElementIndex(labels[index], prefix, formCount);
            }

            let label_name = row.getElementsByTagName('label')[0];
            label_name.innerText = ("ODA " + (formCount + 1));

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
                $('#id_form-'+formCount+'-oda_name').selectize({
                    maxItems: 1,
                    labelField: 'name',
                    valueField: 'name',
                    searchField: 'name',
                    hideSelected: true,
                    persist: false,
                    createOnBlur: true,
                    create: function(input) {
                        return {
                            value: input,
                            name: input
                        }
                    },
                    options: odaList,
                    preload: false,
                    onInitialize: function(){
                        let selectize = this;
                        selectize.setValue(self_oda_selectize[x])
                    }
                });

                let input_delete = row.getElementsByClassName('selectize-control');
                input_delete[1].remove();

        } // End if
        else {
            swal("Error", "Sorry, you can only enter a maximum of 8 items.", "error");
        }
        return false;
    }
    // Register the click event handlers
    $("#add").click(function () {
        return addForm(this, "form");
    });

    $(".delete").click(function () {
        return deleteForm(this, "form");
    });
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
    result = true;
    let inputs = $("form input[type='file']");
    for (let i=0; i<inputs.length; i++) {
        if(inputs[i].files.length>0){
            let image_size = inputs[i].files[0].size / 1024 / 1024;
            if (image_size > 10) {
                swal("Error", "El archivo de seleccionado excede los 10 MB", "error");
                result = false;
                break;
            }
        }


    }


    if (result){

        let inputs_text = [];
        $("form input[type='text']").each(function(){
            inputs_text.push($(this).val());
        });

        for (let i=0; i<inputs_text.length-1; i++) {
            let content=inputs_text[i];
            let value_found = inputs_text.filter((inp) => inp==content);
            if (value_found.length>1){
                swal("Error", "Una ODA solo puede seleccionarse una vez", "error");
                result = false;
                break;
            }
        }
    }
    return result;
}
