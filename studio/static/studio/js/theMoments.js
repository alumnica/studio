$('#h5p-upload').change( function(){
    var filename = $('#h5p-upload').val().split('\\').pop();

    $('#fileName').html(filename);
});


// Tags Materias

var momentoTags = [
    {name: 'tag2', value: 't2'},
    {name: 'tag1', value: 't1'},
    {name: 'tag3', value: 't3'},
    {name: 'cosa', value: 'cs'},
    {name: 'tag5', value: 't5'},
    {name: 'OTHER', value: 'ot'},
    {name: 'tag7', value: 't7'},
];

$('#momento-tags').selectize({
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
    options: momentoTags,
    preload: false,
    maxItems: 20,
    maxOptions: 3,
});