
$(document).ready(function () {
    // Code adapted from http://djangosnippets.org/snippets/1389/
    var x = 0;

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
            var selectize = this;
            selectize.setValue(self_oda_selectize[x])
        }
    });
    x++;
});

    function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+-)');
        var replacement = prefix + '-' + ndx + '-';
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
        replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function deleteForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (formCount > 1) {
            // Delete the item/form
            $(btn).parents('.my_item').remove();
            var forms = $('.my_item'); // Get all the forms
            // Update the total number of forms (1 less than before)
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            // Go through the forms and set their indices, names and IDs
            var inputs = row.getElementsByTagName('input');
            for (index = 0; index < inputs.length; ++index) {
                updateElementIndex(inputs[index], prefix, formCount);
                $(inputs[index]).val("");
            }
            var labels = row.getElementsByTagName('label');
            for (index = 0; index < labels.length; ++index) {
                updateElementIndex(labels[index], prefix, formCount);
            }

            var images = row.getElementsByTagName('img');
            for (index = 0; index < images.length; ++index) {
                updateElementIndex(images[index], prefix, formCount);
                $(images[index]).removeAttr('src')
            }
        } // End if
        else {
            alert("You have to enter at least one todo item!");
        }
        return false;
    }

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                var cosa = '#preview-' + $(input).attr('name');
                $(cosa).attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    }

    function addForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        // You can only submit a maximum of 10 todo items
        if (formCount < 8) {
            // Clone a form (without event handlers) from the first form
            var row = $(".my_item:first").clone(false).get(0);

            var inputs = row.getElementsByTagName('input');
            for (index = 0; index < inputs.length; ++index) {
                updateElementIndex(inputs[index], prefix, formCount);
                $(inputs[index]).val("");
                 if ($(inputs[index]).is( "[type=file]" ) ) {
                    $(inputs[index]).change(function () {
                        readURL(this);
                    });
        }
            }
            var labels = row.getElementsByTagName('label');
            for (index = 0; index < labels.length; ++index) {
                updateElementIndex(labels[index], prefix, formCount);
            }

            var label_name = row.getElementsByTagName('label')[0];
            label_name.innerText = ("ODA " + (formCount + 1));

            var images = row.getElementsByTagName('img');
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
                        var selectize = this;
                        selectize.setValue(self_oda_selectize[x])
                    }
                });

                var input_delete = row.getElementsByClassName('selectize-control');
                input_delete[1].remove();

        } // End if
        else {
            alert("Sorry, you can only enter a maximum of ten items.");
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

function is_valid_form (){
    var position_inputs = document.getElementsByTagName('input');

    for(var i = 0; i < position_inputs.length; i++){
        if(position_inputs[i].value == "" || position_inputs[i].value == null){
            swal("Error", "Coloca todas las ODAs en la imagen de sección", "error");
            return false;
        }
    }
    return true;

}