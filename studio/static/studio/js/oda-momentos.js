
 // enable selectize for all inputs in modals

 $('#select-momentos').selectize({
    maxItems: 1,
    labelField: 'name',
    valueField: 'code',
    searchField: 'name',
    options: momentosList,
    preload: true,
});

//enable sortable for all 6 uodas
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



//pasa la evaluacion  elegida en el modal a la lista sorteable en ambitos-edit
$("#eval-adder").click(function (e) {
    e.preventDefault();
    // var text = $("#eval-select").text();
    var value = $("#eval-select").val();
    // var uodaToGo = $('#Modal-1').attr('uoda');

    $('#eval ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+value+'"></i>' + value + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
    $('#eval ul').sortable('refresh');
    if ($('#eval ul li').length > 4) {
        $('#eval .add-materia').hide();
    }
});


// enable and disable button to add oda
$('#eval-select').change(function () {
    if (!$("#eval-select").val()) {
        $('#eval-adder').prop("disabled", true);
    }
    else {
        $('#eval-adder').prop("disabled", false);
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
        $('#apli-momentos').val(apliTexts.join('|'));
    });

    $(function () {
        $('#uoda-2 li').each(function () {
            formaTexts.push($(this).text());
        });

        // send to hidden input
        $('#forma-momentos').val(formaTexts.join('|'));
    });

    $(function () {
        $('#uoda-3 li').each(function () {
            activTexts.push($(this).text());
        });

        // send to hidden input
        $('#activ-momentos').val(activTexts.join('|'));
    });

    $(function () {
        $('#uoda-4 li').each(function () {
            ejemTexts.push($(this).text());
        });

        // send to hidden input
        $('#ejem-momentos').val(ejemTexts.join('|'));
    });

    $(function () {
        $('#uoda-5 li').each(function () {
            sensTexts.push($(this).text());
        });

        // send to hidden input
        $('#sens-momentos').val(sensTexts.join('|'));
    });

    $(function () {
        $('#uoda-6 li').each(function () {
            evalTexts.push($(this).text());
        });

        // send to hidden input
        $('#eval-momentos').val(evalTexts.join('|'));
    });

});

