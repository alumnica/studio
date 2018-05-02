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


// Tags odas

var odaTags = [
    {name: 'tag2', value: 't2'},
    {name: 'tag1', value: 't1'},
    {name: 'tag3', value: 't3'},
    {name: 'cosa', value: 'cs'},
    {name: 'tag5', value: 't5'},
    {name: 'OTHER', value: 'ot'},
    {name: 'tag7', value: 't7'},
];

$('#oda-tags').selectize({
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
    options: odaTags,
    preload: false,
    maxItems: 20,
});