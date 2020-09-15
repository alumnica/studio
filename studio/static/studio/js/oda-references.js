// Tags odas
$('#oda-references').selectize({
    labelField: 'name',
    valueField: 'name',
    searchField: 'name',
    hideSelected: true,
    persist: false,
    createOnBlur: true,
    delimiter: '|',
    create: function(input) {
        return {
            value: input,
            name: input
        }
    },
    options: odaReferences,
    preload: false,
    maxItems: 20,
    onInitialize: function(){
    let selectize = this;
    selectize.setValue(self_references_selectize)
    }
});


