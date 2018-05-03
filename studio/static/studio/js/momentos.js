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
    $("#uoda-1, #uoda-2, #ouda-3, #uoda-4, #uoda-5, #uoda-6").sortable();
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

    $('#'+uodaToGo+' ul').append('<li class="momento-item"><i class="fas fa-external-link-alt mom-preview" data-open="Modal-2" data-url="'+value+'"></i> ' + text + ' <span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
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
