$(document).ready(function () {
    if(self_subject != "" && self_subject!= null){
        $('#materia-list').val(self_subject);
        $('#materia-list').trigger('change');

        if(self_subject != "" && self_subject!= null){
            $('#oda-list').val(self_oda);
            $('#oda-list').trigger('change');


            if(self_subject != "" && self_subject!= null){
            $('#micro-oda').val(self_microoda);
            $('#micro-oda').trigger('change');
            }
        }

    }
    if(file_name != "" && file_name != null){
        file_name = file_name.split('?');
        $('#fileName').html(file_name[0]);
    }

});


$('#h5p-upload').change( function(){
    let value =  $('#h5p-upload');
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
         swal("Error", "Introduce un nombre", 'error');
         return false;
     }

     let subject = document.getElementById('materia-list').value;
     if (subject == "" || subject == null){
         swal("Error", "Selecciona una materia", 'error');
         return false;
     }

     let oda = document.getElementById('oda-list').value;
     if (oda == "" || oda == null){
         swal("Error", 'Selecciona un ODA', 'error');
         return false;
     }

     let microoda = document.getElementById('micro-oda').value;
     if (microoda == "" || microoda == null){
         swal("Error", "Selecciona un MicroODA", 'error');
         return false;
     }

     let moment_type = document.getElementById('tipo-momento').value;
     if (moment_type == "" || moment_type == null){
         swal("Error", "Selecciona el tipo de momento", 'error');
         return false;
     }

     let tags = document.getElementById('momento-tags').value;
     if (tags == "" || tags == null){
         swal("Error", "Escribe al menos un tag", 'error');
         return false;
     }

     let url = gettext('/api/zip_files/');
     let control = document.getElementById('h5p-upload');
     let data = $('#h5p-upload').val();
     let previous_file = $('#fileName').html();

     if ((data == "" || data == null) && (previous_file == "" || previous_file == null))
     {
         swal("Error", "Selecciona un archivo H5P", 'error');
         return false;
     }



    if (data != "" && data != null){
         let match_found = data.search('.h5p');
         if(match_found == -1){
            swal("Error", "Selecciona un archivo H5P", "error");
            return false;
         }
        swal({
        title: 'Please wait',
        allowOutsideClick: false,
        });
        swal.showLoading();
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
              swal.close();
              swal("Error", "El archivo no pudo subirse, por favor intenta más tarde", 'error');
          }
        });
    }
    else{
        $('#uploadForm').submit();
    }

 });

/**
 * First call looking up for job status
 * @param data
 * @returns {boolean}
 */
 function success(data){

    if (data.status == "error"){
        swal("Error", data.error, 'error');
        return false;
    }
    $('#url_h5p').val(data.job.package_job_id);
    url_status = data.job.job_url;

    $.ajax({
      type: "GET",
      url: url_status,
      success: lookUpURL,
      error: function(data){
          swal.close();
          swal("Error", "El archivo no pudo subirse, por favor intenta más tarde", 'error');
      },
      dataType: 'text'
    });

    /**
     * Reviews job status to keep asking for h5p file uploading task
     * @param data
     * @returns {boolean}
     */
    function lookUpURL(data) {
    let data_info = JSON.parse(data);
    if (data_info.is_failed){
        swal.close();
        swal("Error", "El archivo no pudo subirse, por favor intenta más tarde", 'error');
        return false;
    }
    if(data_info.is_finished){

        $('#uploadForm').submit();
        swal.close();
        return false;
    }
    setTimeout(get_url, 1000)
}

    /**
     * Asks for job status
     */
    function get_url() {
    $.ajax({
      type: "GET",
      url: url_status,
      success: lookUpURL,
      error: function(data){
          swal.close();
          swal("Error", "El archivo no pudo subirse, por favor intenta más tarde", 'error');
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
    onInitialize: function() {
        let selectize = this;
        selectize.setValue(self_tags_selectize)
    },
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
    onInitialize: function() {
        let selectize = this;
        selectize.setValue(self_type)
    },
    maxOptions: 4,
});
