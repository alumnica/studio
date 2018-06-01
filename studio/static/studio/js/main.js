
// cambiar texto de el image preview al escribir

$('#id_name').keyup(function () {
    let textToChange = $(this).val();
    $('.ttc2').text(textToChange);
});

// cambia los colers de el image preiew al dar click en el color

$('#color-button input[type=radio]').click(function () {
    let $this = $(this);
    $('#image-holder').attr('class', $this.data('a'));
    $('#ttc').attr('class', $this.data('b'));
});

//Sortable Materias en creacion de  Ambitos

$(function () {
    $("#sortable").sortable();
    // $( "#sortable" ).disableSelection();
    // deprecated
});



let numMateria = 1;

// anadir materias en Ambito-edit

$(document).ready(function () {
    $('#select-materias').change(function () {
        if (!$("select[name='materias-select']").val()) {

            $('#class-adder').prop("disabled", true);
        }
        else {

            $('#class-adder').prop("disabled", false);
        }
    });
});

//pasa la materia elegida en el modal a la lista sorteable en ambitos-edit



// pasa el orden de las materias en ambitos-edit a un text input escondido
// para que en post tengamos al info correcta

$('#last_panel').on('mouseenter mouseleave', function () {

    let texts = [];

    $(function () {
        $('#sortable li').each(function () {
            texts.push($(this).text());
        });

        // alert(texts);
        $('#class_name').val(texts);
    });

});

// alphanum for all inputs

$("input").alphanum({
    allow :    ',-_',
});

// quit alphanum
$('#id_email, #id_password').off('.alphanum');
// Image file upload preview for Materias

$(document).ready(function () {
    let i = 0;
    let y = 0;

    // Materias-edit-seccion.html
    $("#seccion-img img").each(function () {
        $(this).attr("id", "preview-form-" + i + "-file");
        i++;

    });

    // materias-edit.html
    $(".materia-preview img").attr({id:"preview-mp", class:"materia-cover is-hidden" });
    // ambitos-edit.html
    $("form#ambito-creation img").attr({id:"preview-ap", class:"ambito-cover is-hidden" });
    // oda-edit
    $("form#oda-edit .active_icon-preview img").attr({id:"preview-active_icon", class:"oda-cover is-hidden"});

    $("form#oda-edit .completed_icon-preview img").attr({id:"preview-completed_icon", class:"oda-cover is-hidden"});
     
});

$(document).ready(function () {

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

    $("#seccion-img input[type='file']").change(function () {
        readURL(this);
    });

    $("#materia-u").change(function () {
        readURL(this);
        $("#preview-mp").removeClass("is-hidden");
    });

    $("#ambito-u").change(function () {
        readURL(this);
        $("#preview-ap").removeClass("is-hidden");
    });
    
    $("#id_active_icon").change(function () {
        readURL(this);
        $("#preview-active_icon").removeClass("is-hidden");

    });

    $("#id_completed_icon").change(function () {
        readURL(this);
        $("#preview-completed_icon").removeClass("is-hidden");
    });
});

$(document).ready(function () {
    $('.selectize-input input[type=text]').attr('maxlength', '20');
     $(".title span").append($("#id_name").val());

});

function is_valid_form_images (){
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
    return result;
}