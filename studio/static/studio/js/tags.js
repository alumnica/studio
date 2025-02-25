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
    preload: false,
    onInitialize: function() {
        let selectize = this;
        selectize.setValue(self_tags_selectize)
    },
    maxItems: 20,
});


// Tags Materias

$('#materias-tags').selectize({
    labelField: 'name',
    valueField: 'name',
    searchField: 'name',
    hideSelected: true,
    persist: false,
    createOnBlur: true,
    maxItems: 20,
    create: function(input) {
        return {
            value: input,
            name: input
        }
    },
    options: materiasTags,
    preload: true,
    onInitialize: function(){
    let selectize = this;
    selectize.setValue(self_tags_selectize)
}
});


