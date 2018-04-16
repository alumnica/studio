
//Selecion de Materias dentro de Ambitos


$('#select-materias').selectize({
    maxItems: 1,
    labelField: 'name',
    valueField: 'name',
    searchField: 'name',
    options: materiasList,
    preload: true
});




//seleccion de ODAS dentro de Ambitos

var odaList = [
    {name: 'ODA-N1'},
    {name: 'ODA-N2'},
    {name: 'ODA-N3'},
    {name: 'ODA-N4'},
    {name: 'ODA-N5'},
    {name: 'ODA-N6'},
    {name: 'ODA-N7'},
];

var x = 0;

$("input[type='text']").each(function(){
    x++;
    $('#section-1-oda-'+x).selectize({
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
    });
});