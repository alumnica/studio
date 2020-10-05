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

    //self_type
    if (self_type!= undefined){
      if ( self_type=='h5p'){
        $('#div_content').hide();
        $('#div_text_free').hide();
        $('#div_question').hide();
        $('#div_hotspots').hide();
        $('#div_h5p').show();
      }
      else if (self_type=='text'){
        $('#div_content').hide();
        $('#div_h5p').hide();        
        $('#div_question').hide();
        $('#div_hotspots').hide();
        $('#div_text_free').show();
      }
      else if (self_type=='question'){
        $('#div_content').hide();
        $('#div_h5p').hide();
        $('#div_text_free').hide();
        $('#div_hotspots').hide();
        $('#div_question').show();
      }
      else if (self_type=='hotspots'){
        $('#div_content').show();
        $('#div_h5p').hide();
        $('#div_text_free').show();        
        $('#div_question').hide();
        $('#div_hotspots').show();
      }

      else { //Img. mp4, gif, timeline, twine
        $('#div_content').show();
        $('#div_h5p').hide();
        $('#div_text_free').hide();  
        $('#div_question').hide();
        $('#div_hotspots').hide();
      }
    }
    
    
    if(file_name != "" && file_name != null){
        file_name = file_name.split('?');
        $('#fileName').html(file_name[0]);
    }

});


$('#content').change( function(){
    let value =  $('#content');
    var filename = $('#content').val().split('\\').pop();

    $('#fileName').html(filename);
});

let url_status = '';

 $('#oda-list').change(function () {
       let oda_name = this.value;
       let oda = oda_microodas.filter(x => x.name === oda_name);
       let microoda = oda[0].microodas;
       let mapping_microodas = {
            'application': 'Integrar', 
            'formalization': 'Modelar',
            'activation': 'Aplicar', 
            'exemplification': 'Explorar', 
            'sensitization': 'Conectar', 
       };
       let select_microodas = $('#micro-oda');
       select_microodas.empty();
       select_microodas.append('<option disabled selected></option>');
       for(let i=0; i<microoda.length; i++){
           option = $('<option></option>').attr("value", microoda[i]).text(mapping_microodas[microoda[i]]);
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

    $('#submit_button').addClass('hide')
    $('#procesando').removeClass('hide')

     let name = document.getElementById('name').value;
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

     
    
    type_moment = document.getElementById('tipo-momento').value;
    

    if (type_moment=="h5p"){
        let frame_url = document.getElementById('url_h5p').value;
        if (frame_url == "" || frame_url == null){
             swal("Error", "Escribe la url del frame", 'error');
             return false;
         }

         let script_url = document.getElementById('library_h5p').value;
         if (script_url == "" || script_url == null){
             swal("Error", "Escribe la url del script", 'error');
             return false;
         }

            //alert ('send only form because type is h5p')
            let url = gettext('/api/content/');
            swal({
              title: 'Please wait',
              allowOutsideClick: false,
            });
            swal.showLoading();
            let formH5P = new FormData($('#uploadForm')[0]);
             
             
            $.ajax({
                type: "POST",
                url: url,
                data: formH5P,
                success: success,
                contentType: false,
                processData: false,
                error: function(data){
                    swal.close();
                    swal("Error", "El content h5p no pudo cargarse, por favor intenta más tarde", 'error');
                }
            }); 
    }
    else if (type_moment=="text"){        

        let text_free = document.getElementById('text_free').value;
        if (text_free == "" || text_free == null){
             swal("Error", "Escribe el texto libre", 'error');
             return false;
         }

         

        //alert ('send only form because type is h5p')
        let url = gettext('/api/content/');
        swal({
          title: 'Please wait',
          allowOutsideClick: false,
        });
        swal.showLoading();
        let formH5P = new FormData($('#uploadForm')[0]);
         
         
        $.ajax({
            type: "POST",
            url: url,
            data: formH5P,
            success: success,
            contentType: false,
            processData: false,
            error: function(data){
                swal.close();
                swal("Error", "El content texto libre no pudo cargarse, por favor intenta más tarde", 'error');
            }
        });        
        
    }

    else if (type_moment=="hotspots"){        

         let text_free = document.getElementById('text_free').value;
        if (text_free == "" || text_free == null){
             swal("Error", "Escribe el texto libre", 'error');
             return false;
         }


         let coordenada1 = document.getElementById('coordenada1').value;
         let coordenada2 = document.getElementById('coordenada2').value;
         let coordenada3 = document.getElementById('coordenada3').value;
         let coordenada4 = document.getElementById('coordenada4').value;
        if ((coordenada1 == "" || coordenada1 == null)&&(coordenada2 == "" || coordenada2 == null)&&
          (coordenada3 == "" || coordenada3 == null)&&(coordenada4 == "" || coordenada4 == null)){
             swal("Error", "Escribe Las coordenadas de la imagen", 'error');
             return false;
         }

        let url = gettext('/api/content/');
        console.log('url ' + url)
        let control = document.getElementById('content');
        let data = $('#content').val();
        let previous_file = $('#fileName').html();

        if ((data == "" || data == null) && (previous_file == "" || previous_file == null))
        {
           swal("Error", "Selecciona un archivo", 'error');
           return false;
        }
        if (data != "" && data != null){
           
            swal({
              title: 'Please wait',
              allowOutsideClick: false,
            });
            swal.showLoading();
               let formH5P = new FormData($('#uploadForm')[0]);
               let inputH5P = $('#content')[0];
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
             //alert ('send only form')
              $('#uploadForm').submit();
          }
        
    }

    else if (type_moment== "question"){        

        let question = document.getElementById('question').value;
        if (question == "" || question == null){
             swal("Error", "Escribe la pregunta", 'error');
             return false;
         }

         let answer1 = document.getElementById('answer1').value;
         let answer2 = document.getElementById('answer2').value;
        if ((answer1 == "" || answer1 == null)&&(answer2 == "" || answer2 == null)){
             swal("Error", "Escribe al menos dos respuesta", 'error');
             return false;
         }

         let positive_retro = document.getElementById('positive_retro').value;
         let negative_retro = document.getElementById('negative_retro').value;
        if ((positive_retro == "" || positive_retro == null)&&(negative_retro == "" || negative_retro == null)){
             swal("Error", "Escribe la retroalimentación para la pregunta", 'error');
             return false;
         }

         let correct_answer = document.getElementById('correct_answer').value;
         console.log (correct_answer)
        if (correct_answer == "" || correct_answer == null){
             swal("Error", "Escribe la respuesta correcta", 'error');
             return false;
         }

                  

        //alert ('send only form because type is h5p')
        let url = gettext('/api/content/');
        swal({
          title: 'Please wait',
          allowOutsideClick: false,
        });
        swal.showLoading();
        let formH5P = new FormData($('#uploadForm')[0]);
         
        $.ajax({
            type: "POST",
            url: url,
            data: formH5P,
            success: success,
            contentType: false,
            processData: false,
            error: function(data){
                swal.close();
                swal("Error", "El content de Pregunta no pudo cargarse, por favor intenta más tarde", 'error');
            }
        });        
        
    }

    else{ //Content file -> mp4, gif, img, twine, timeline

        let url = gettext('/api/content/');
          console.log('url ' + url)
          let control = document.getElementById('content');
          let data = $('#content').val();
          let previous_file = $('#fileName').html();

          if ((data == "" || data == null) && (previous_file == "" || previous_file == null))
          {
             swal("Error", "Selecciona un archivo", 'error');
             return false;
          }
          if (data != "" && data != null){
              
              swal({
                title: 'Please wait',
                allowOutsideClick: false,
              });
              swal.showLoading();
                 let formH5P = new FormData($('#uploadForm')[0]);
                 let inputH5P = $('#content')[0];
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
             //alert ('send only form')
              $('#uploadForm').submit();
          }

                   
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
    
    //alret ('se va guardar la forma 2')
    swal.close();
    $('#id_content').val(data.url.split("/")[5]);

    //alert ('se va guardar la forma')
    $('#uploadForm').submit();
    return false;
  

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
    maxOptions: 10,
});

$('#correct_answer').selectize({
    maxItems: 1,
    labelField: 'name',
    valueField: 'name',
    searchField: 'name',
    options: answersList,
    preload: true,
    onInitialize: function() {
        let selectize = this;
        selectize.setValue(correct_answer)
    },
    maxOptions: 4,
});


$('#tipo-momento').change(function () {
      let type_name = this.value;
      //alert ('change type ' + type_name);
      

      if ( type_name=='h5p'){
        $('#div_content').hide();
        $('#div_text_free').hide();
        $('#div_question').hide();
        $('#div_hotspots').hide();
        $('#div_h5p').show();
      }
      else if (type_name=='text'){
        $('#div_content').hide();
        $('#div_h5p').hide();        
        $('#div_question').hide();
        $('#div_hotspots').hide();
        $('#div_text_free').show();
      }
      else if (type_name=='question'){
        $('#div_content').hide();
        $('#div_h5p').hide();
        $('#div_text_free').hide();
        $('#div_hotspots').hide();
        $('#div_question').show();
      }
      else if (type_name=='hotspots'){
        $('#div_content').show();
        $('#div_h5p').hide();
        $('#div_text_free').show();        
        $('#div_question').hide();
        $('#div_hotspots').show();
      }

      else { //Img. mp4, gif, timeline, twine
        $('#div_content').show();
        $('#div_h5p').hide();
        $('#div_text_free').hide();  
        $('#div_question').hide();
        $('#div_hotspots').hide();
      }

   });
