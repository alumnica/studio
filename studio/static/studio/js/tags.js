//Tags Ambitos


$('#ambito-tags').selectize({
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
    options: ambitoTags,
    preload: false
});


// Tags Materias

$('#materias-tags').selectize({
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
    options: materiasTags,
    preload: true,
    onInitialize: function(){
    var selectize = this;
    selectize.setValue(self_tags_selectize)


}
});
