
//Selecion de Materias dentro de Ambitos

var materiasList = [ 
    {name: 'Alquimia', code: 'AF'}, 
    {name: 'Brujeria', code: 'AX'}, 
    {name: 'Astrologia', code: 'AL'},
];

$('#select-materias').selectize({
    maxItems: 1,
    labelField: 'name',
    valueField: 'name',
    searchField: 'name',
    options: materiasList,
    preload: true,
});