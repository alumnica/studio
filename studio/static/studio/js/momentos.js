// seleccion de momentos dentro de Oda-edit


 // enable selectize for all inputs in modals

 $('#select-momentos').selectize({
    maxItems: 1,
    labelField: 'name',
    valueField: 'code',
    searchField: 'name',
    options: momentosList,
    preload: true,
});

//enable sortable for all 6 udas
$(function () {
    $("#uoda-1, #uoda-2, #uoda-3, #uoda-4, #uoda-5, #uoda-6").sortable();
    // $( "#sortable" ).disableSelection();
    // deprecated
});

// enable and disable button to add oda
$('#select-momentos').change(function () {
    if (!$("#select-momentos").val()) {
        $('#momento-adder').prop("disabled", true);
    }
    else {
        $('#momento-adder').prop("disabled", false);
    }
});


$('.add-materia').on('click', function(){
    $('#Modal-1').attr('uoda', $(this).parent().parent().attr('id'));
});


//pasa la materia elegida en el modal a la lista sorteable en ambitos-edit
$("#momento-adder").click(function (e) {
    e.preventDefault();
    var text = $("#select-momentos").text();
    var value = $("#select-momentos").val();
    var uodaToGo = $('#Modal-1').attr('uoda');

    $('#'+uodaToGo+' ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+value+'"></i>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
    $('#'+uodaToGo+' ul').sortable('refresh');
    if ($('#'+uodaToGo+' ul li').length > 4) {
        $('#'+uodaToGo+' .add-materia').hide();
    }
});

$(".oda-sort").on('click', '.remove_materia', function () {
    $(this).parent().remove();
    if ($(this).parent().length < 4) {
        $('.add-materia').show();
    }
});


$('.oda-sort').on('click', '.mom-preview', function(){
    var iUrl = $(this).attr('data-url');
    $('iframe').attr('src', iUrl);

    
});

// pasa el orden de los momentos en cada uoda a su text input escondido
// para que en post tengamos al info correcta

$('#save-on').on('mouseenter mouseleave', function () {

    var apliTexts = [],
        formaTexts = [],
        activTexts = [],
        ejemTexts = [],
        sensTexts = [],
        evalTexts = [];


    $(function () {
        $('#uoda-1 li').each(function () {
            apliTexts.push($(this).text());
        });

        // send to hidden input
        $('#apli-momentos').val(apliTexts);
    });

    $(function () {
        $('#uoda-2 li').each(function () {
            formaTexts.push($(this).text());
        });

        // send to hidden input
        $('#forma-momentos').val(formaTexts);
    });

    $(function () {
        $('#uoda-3 li').each(function () {
            activTexts.push($(this).text());
        });

        // send to hidden input
        $('#activ-momentos').val(activTexts);
    });

    $(function () {
        $('#uoda-4 li').each(function () {
            ejemTexts.push($(this).text());
        });

        // send to hidden input
        $('#ejem-momentos').val(ejemTexts);
    });

    $(function () {
        $('#uoda-5 li').each(function () {
            sensTexts.push($(this).text());
        });

        // send to hidden input
        $('#sens-momentos').val(sensTexts);
    });

    $(function () {
        $('#uoda-6 li').each(function () {
            evalTexts.push($(this).text());
        });

        // send to hidden input
        $('#eval-momentos').val(evalTexts);
    });

});

$(document).ready(function () {
    for (let i=0; i<apli.length; i++){
        var text = apli[i].name;
        var value = apli[i].code;


        $('#apli ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+value+'"></i>'  + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#apli ul').sortable('refresh');
        if ($('#apli ul li').length > 4) {
            $('#apli .add-materia').hide();
        }
    }

    for (let i=0; i<forma.length; i++){
        var text = forma[i].name;
        var value = forma[i].code;

        $('#forma ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+value+'"></i>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#forma ul').sortable('refresh');
        if ($('#forma ul li').length > 4) {
            $('#forma .add-materia').hide();
        }
    }

    for (let i=0; i<activa.length; i++){
        var text = activa[i].name;
        var value = activa[i].code;

        $('#activ ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+value+'"></i>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#activ ul').sortable('refresh');
        if ($('#activ ul li').length > 4) {
            $('#activ .add-materia').hide();
        }
    }
    for (let i=0; i<ejem.length; i++){
        var text = ejem[i].name;
        var value = ejem[i].code;

        $('#ejemp ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+value+'"></i>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#ejemp ul').sortable('refresh');
        if ($('#ejemp ul li').length > 4) {
            $('#ejemp .add-materia').hide();
        }
    }

    for (let i=0; i<sens.length; i++){
        var text = sens[i].name;
        var value = sens[i].code;

        $('#sens ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+value+'"></i>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#sens ul').sortable('refresh');
        if ($('#sens ul li').length > 4) {
            $('#sens .add-materia').hide();
        }
    }

    for (let i=0; i<evalu.length; i++){
        var text = evalu[i].name;
        var value = evalu[i].code;

        $('#eval ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+value+'"></i>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
        $('#eval ul').sortable('refresh');
        if ($('#eval ul li').length > 4) {
            $('#eval .add-materia').hide();
        }
    }
});