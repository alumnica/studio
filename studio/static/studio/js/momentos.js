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

 $('#submit_button').on('click', function () {

     let name = document.getElementById('h5p-name').value;
     if (name == "" || name == null){
         swal("Error", gettext('The name field is required'), 'error');
         return;
     }

     let subject = document.getElementById('materia-list').value;
     if (subject == "" || subject == null){
         swal("Error", gettext('The subject field is required'), 'error');
         return;
     }

     let oda = document.getElementById('oda-list').value;
     if (oda == "" || oda == null){
         swal("Error", gettext('The ODA field is required'), 'error');
         return;
     }

     let microoda = document.getElementById('micro-oda').value;
     if (microoda == "" || microoda == null){
         swal("Error", gettext('The Micro ODA field is required'), 'error');
         return;
     }

     let moment_type = document.getElementById('tipo-momento').value;
     if (moment_type == "" || moment_type == null){
         swal("Error", gettext('Select the moment type'), 'error');
         return;
     }

     let tags = document.getElementById('momento-tags').value;
     if (tags == "" || tags == null){
         swal("Error", gettext('Introduce at least one tag'), 'error');
         return;
     }

     let url = '';
     let data = $('#h5p-upload').val();

     if (data == "" || data == null){
         swal("Error", gettext('Any file has been selected'), 'error');
         return;
     }
     let match_found = data.search('.h5p');
     if(match_found == -1){
        swal("Error", gettext("Select a H5P file"), "error");
        return false;
     }

     $.ajax({
      type: "POST",
      url: url,
      data: data,
      success: success,
      dataType: 'text'
    });
 });

 function success(data){
    $('#url_h5p').val(data);
    if (data!= "" || data!=null){
        $('#uploadForm').submit();
    }
    else{
        swal("Error", gettext('Sorry there was an error uploading you file, try later'), 'error');
    }
 }

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
