
//Selecion de Materias dentro de Ambitos


$('#select-materias').selectize({
    maxItems: 1,
    labelField: 'name',
    valueField: 'name',
    searchField: 'name',
    options: materiasList,
    preload: true
});



