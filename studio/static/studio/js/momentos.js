$('#h5p-upload').change( function(){
    var filename = $('#h5p-upload').val().split('\\').pop();

    $('#fileName').html(filename);
});


 $('#oda-list').change(function () {
       let oda_name = this.value;
       let oda = oda_microodas.filter(x => x.name === oda_name);
       let microoda = oda[0].microodas;
       let select_microodas = $('#micro-oda');
       select_microodas.empty();
       select_microodas.append('<option disabled selected></option>');
       for(let i=0; i<microoda.length; i++){
           option = $('<option></option>').attr("value", microoda[i]).text(microoda[i]);
           select_microodas.append(option);
       }
   });


 $('#materia-list').change(function () {
       let subject_name = this.value;
       let subject = subject_odas.filter(x => x.name === subject_name);
       let odas = subject[0].odas;
       let select_odas = $('#oda-list');
       select_odas.empty();
       select_odas.append('<option disabled selected></option>');
       for(let i=0; i<odas.length; i++){
           option = $('<option></option>').attr("value", odas[i].name).text(odas[i].name);
           select_odas.append(option);
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


$('#tipo-momento').selectize({
    maxItems: 1,
    labelField: 'name',
    valueField: 'name',
    searchField: 'name',
    options: typeList,
    preload: true,
    maxOptions: 4,
});
