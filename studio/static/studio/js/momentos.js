$('#h5p-upload').change( function(){
    var filename = $('#h5p-upload').val().split('\\').pop();

    $('#fileName').html(filename);
});


 $('#oda-list').change(function () {
       oda_name = this.value;

       oda = oda_microodas.filter(x => x.name === oda_name);
       microoda = oda[0].microodas;
       select_microodas = $('#micro-oda');
       select_microodas.empty();
       for(let i=0; i<microoda.length; i++){
           option = $('<option></option>').attr("value", microoda[i]).text(microoda[i]);
           select_microodas.append(option);
       }
   });


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



/*$('#oda-list').selectize({
    maxItems: 1,
    labelField: 'name',
    valueField: 'name',
    searchField: 'name',
    options: odaList,
    preload: true,
});*/



// list of tipos de momentos

var typeList = [ 
    {name: 'Tipo A'}, 
    {name: 'Tipo B'}, 
    {name: 'Tipo C'}, 
    {name: 'Tipo D'}, 
    {name: 'Tipo E'}, 
    {name: 'Tipo F'}, 
    {name: 'Tipo G'}, 
    
];

$('#tipo-momento').selectize({
    maxItems: 1,
    labelField: 'name',
    valueField: 'name',
    searchField: 'name',
    options: typeList,
    preload: true,
    maxOptions: 4,
});
