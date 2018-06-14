$('#h5p-upload').change( function(){
    var filename = $('#h5p-upload').val().split('\\').pop();

    $('#fileName').html(filename);
});
let url_status = '';

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

     let url = 'https://django-h5p.herokuapp.com/api/zip_files/';
     let control = document.getElementById('h5p-upload');
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

    let formH5P = new FormData($('#uploadForm')[0]);
     let inputH5P = $('#h5p-upload')[0];
     formH5P.append('package', inputH5P.files[0]);
     $.ajax({
      type: "POST",
      url: url,
      data: formH5P,
      success: success,
      contentType: false,
      processData: false,
      error: function(data){
          swal("Error", gettext("Failed loading the file, please try later"), 'error');
      }
    });
 });

 function success(data){

    if (data.status == "error"){
        swal("Error", data.error, 'error');
        return;
    }
    $('#url_h5p').val(data.job.package_url);
    url_status = data.job.job_url;
    swal('Please wait');
    swal.showLoading();
    $.ajax({
      type: "GET",
      url: url_status,
      success: lookUpURL,
      error: function(data){
          swal("Error", gettext("Failed loading the file, please try later"), 'error');
      },
      dataType: 'text'
    });

function lookUpURL(data) {
    let data_info = JSON.parse(data);
    if (data_info.is_failed){
        swal.close();
        swal("Error", gettext("Failed loading the file, please try later"), 'error');
        return;
    }
    if(data_info.is_finished){
        swal.close();

        $('#uploadForm').submit();
        return;
    }
    setTimeout(get_url, 1000)
}

function get_url() {
    $.ajax({
      type: "GET",
      url: url_status,
      success: lookUpURL,
      error: function(data){
          swal.close();
          swal("Error", gettext("Failed loading the file, please try later"), 'error');
      },
      dataType: 'text'
    });
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
