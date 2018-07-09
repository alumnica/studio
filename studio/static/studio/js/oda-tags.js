// Tags odas


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
    onInitialize: function(){
    let selectize = this;
    selectize.setValue(self_tags_selectize)
    }
});

// uoda TAGS



$('#apli-tags, #forma-tags, #activ-tags, #ejemp-tags, #sens-tags').selectize({
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
    maxItems: 10,
    onInitialize: function(){
    let selectize = this;
    selectize.setValue(self_tags_selectize)
    }
});
