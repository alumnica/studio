// seleccion de momentos dentro de Oda-edit

var momentosList = [ 
    {name: 'Momento A', code: 'AF'}, 
    {name: 'Slideshow X', code: 'AX'}, 
    {name: 'Hostspot Y', code: 'AL'},
];

$('#select-momentos').selectize({
    maxItems: 1,
    labelField: 'name',
    valueField: 'name',
    searchField: 'name',
    options: momentosList,
    preload: true,
});

// add Sortable to the lists

$(function () {
    
    $("#oda-sort-1, #oda-sort-2, #oda-sort-3").sortable();
    // $( "#sortable" ).disableSelection();
    // deprecated
});


// enable and disable button to add oda

$('#select-momentos').change(function () {
    if (!$("select[name='momentos-select']").val()) {

        $('#momento-adder').prop("disabled", true);
    }
    else {

        $('#momento-adder').prop("disabled", false);
    }
});

//pasa la materia elegida en el modal a la lista sorteable en ambitos-edit

$("#momento-adder").click(function (e) {
    e.preventDefault();

    var text = $("select[name='momentos-select']").val();

    $("#oda-sort-1").append('<li class="momento-item"><i class="fas fa-external-link-alt"></i> ' + text + ' <span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
	
    $("#oda-sort-1").sortable('refresh');
    if ($('ul#oda-sort-1 li').length > 6) {
        $('#add-materia-button').hide();
    }


});

$("#oda-sort-1").on('click', '.remove_materia', function () {
    $(this).parent().remove();
    if ($('ul#oda-sort-1 li').length < 7) {
        $('#add-materia-button').show();
    }
});