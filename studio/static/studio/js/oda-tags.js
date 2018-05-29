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

$(document).ready(function () {
   $('#materia-a-oda').change(function () {
       subject_name = this.value;

       subject = subject_bloques.filter(x => x.name === subject_name);
       bloques = subject[0].bloques;
       select_bloques = $('#bloque-a-oda');
       select_bloques.empty();
       select_bloques.prepend('<option disabled selected></option>');
       for(let i=0; i<bloques.length; i++){
           option = $('<option></option>').attr("value", bloques[i]).text(bloques[i]);
           select_bloques.append(option);
       }
   });
});