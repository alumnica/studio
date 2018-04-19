
$('#tabla-ambitos').DataTable({
    responsive: true,
    "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
    },
    "columnDefs": [
        { "orderable": false, "targets": [2, 3, 4] }
    ],

});

$('#tabla-materias').DataTable({
    responsive: true,
    "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
    },
    "columnDefs": [
        { "orderable": false, "targets": [2] }
    ],

});


// cambiar texto de el image preview al escribir

$('#id_name_field').keyup(function () {
    var textToChange = $(this).val();
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


$("#sortable").on('click', '.remove_materia', function () {
    $(this).parent().remove();
    if ($('ul#sortable li').length < 4) {
        $('#add-materia-button').show();
    }
});

var numMateria = 1;

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

$("#class-adder").click(function (e) {
    e.preventDefault();

    var text = $("select[name='materias-select']").val();

    $("#sortable").append('<li class="ui-state-default"><span class="ui-icon ui-icon-arrowthick-2-n-s sorter"></span>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
    $("#sortable").sortable('refresh');
    if ($('ul#sortable li').length > 3) {
        $('#add-materia-button').hide();
    }


});

// pasa el orden de las materias en ambitos-edit a un text input escondido
// para que en post tengamos al info correcta

$('#last_panel').on('mouseenter mouseleave', function () {

    var texts = [];

    $(function () {
        $('#sortable li').each(function () {
            texts.push($(this).text());
        });

        // alert(texts);
        $('#class_name').val(texts);
    });

});

// alphanum for all inputs

$("input").alphanum();

// quita alphanum
$('#id_email, #id_password').off('.alphanum');
// Image file upload preview for Materias

$(document).ready(function () {
    var i = 0;
    var y = 0;

    // Materias-edit-seccion.html
    $("form#seccion-img img").each(function () {
        $(this).attr("id", "preview-form-" + i + "-file_field");
        i++;

    });

    // materias-edit.html
    $("form#materia-init img").attr({id:"preview-mp", class:"materia-cover" });
    // ambitos-edit.html
    $("form#ambito-creation img").attr({id:"preview-ap", class:"ambito-cover" });
    // materias-edit-oda
    $("form#odas-seccion-1 .img-preview-a img").each(function () {
        $(this).attr("id", "preview-form-" + i + "-active_icon_field");
        i++;        
    });

    $("form#odas-seccion-1 .img-preview-b img").each(function () {
        $(this).attr("id", "preview-form-" + y + "-completed_icon_field");
        y++;
    });
});

$(document).ready(function () {

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

    $("form#seccion-img input[type='file']").change(function () {
        readURL(this);
    });

    $("#materia-u").change(function () {
        readURL(this);
    });

    $("#ambito-u").change(function () {
        readURL(this);
    });

    $("form#odas-seccion-1 input[type='file']").change(function () {
        readURL(this);
    });
});

$(document).ready(function () {
    $('.selectize-input input[type=text]').attr('maxlength', '20');
    
});