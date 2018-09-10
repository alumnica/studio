
//Selección de Materias dentro de Ambitos


var $select = $('#select-materias').selectize({
    maxItems: 1,
    labelField: 'name',
    valueField: 'name',
    searchField: 'name',
    options: materiasList,
    preload: true
});

let selectize = $select[0].selectize;

$(".fa-plus-square").on('click', function(){
       	selectize.clearOptions();
        selectize.addOption(materiasList);
});


$("#class-adder").click(function () {
//    e.preventDefault();

    let text = $("select[name='materias-select']").val();

    materiasList = materiasList.filter(x => x.name != text);
    $("#sortable").append('<li class="ui-state-default"><span class="ui-icon ui-icon-arrowthick-2-n-s sorter"></span>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
    $("#sortable").sortable('refresh');
    if ($('ul#sortable li').length > 3) {
        $('#add-materia-button').hide();
    };

});

$("#sortable").on('click', '.remove_materia', function () {

    let subject = $(this).parent().contents().filter(function() {
         return this.nodeType == 3;
		}).text();


	var reAdd = {
	"name": subject
	};

    materiasList.push(reAdd);


    $(this).parent().remove();
        if ($('ul#sortable li').length < 4) {
            $('#add-materia-button').show();
        }
});



