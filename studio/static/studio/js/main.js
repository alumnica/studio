// cambiar texto de el image preview al escribir

$('#id_name').keyup(function() {
  let textToChange = $(this).val();
  $('.ttc2').text(textToChange);
});

// cambia los colores de el image preview al dar click en el color

$('#color-button input[type=radio]').click(function() {
  let $this = $(this);
  $('#image-holder').attr('class', $this.data('a'));
  $('#ttc').attr('class', $this.data('b'));
});

//Sortable Materias en creación de  Ambitos

$(function() {
  $('#sortable').sortable();
  // $( "#sortable" ).disableSelection();
  // deprecated
});

let numMateria = 1;

// añadir materias en Ambito-edit

$(document).ready(function() {
  $('#select-materias').change(function() {
    if (!$("select[name='materias-select']").val()) {
      $('#class-adder').prop('disabled', true);
    } else {
      $('#class-adder').prop('disabled', false);
    }
  });
});

//pasa la materia elegida en el modal a la lista sorteable en ambitos-edit

// pasa el orden de las materias en ambitos-edit a un text input escondido
// para que en post tengamos al info correcta

// alphanum for all inputs

$('input').alphanum({
  allow: ',-_',
});

// quit alphanum
$('#id_email, #id_password , #url_h5p , #library_h5p').off('.alphanum');
// Image file upload preview for Materias

$(document).ready(function() {
  let i = 0;
  let y = 0;

  // Materias-edit-seccion.html
  $('#seccion-img img').each(function() {
    $(this).attr('id', 'preview-form-' + i + '-file');
    i++;
  });

  // materias-edit.html
  $('.materia-preview img').attr({
    id: 'preview-mp',
    class: 'materia-cover is-hidden',
  });
  // ambitos-edit.html
  $('#image-holder img').attr({
    id: 'preview-ap',
    class: 'ambito-cover is-hidden',
  });

  $('#badge-a-holder img').attr({
    id: 'preview-aU',
    class: 'badge-preview  is-hidden',
  });
  $('#badge-b-holder img').attr({
    id: 'preview-bU',
    class: 'badge-preview  is-hidden',
  });
  $('#badge-c-holder img').attr({
    id: 'preview-cU',
    class: 'badge-preview  is-hidden',
  });
  // oda-edit
  $('form#oda-edit .active_icon-preview img').attr({
    id: 'preview-active_icon',
    class: 'oda-cover is-hidden',
  });

  $('form#oda-edit .completed_icon-preview img').attr({
    id: 'preview-completed_icon',
    class: 'oda-cover is-hidden',
  });
});

$(document).ready(function() {
  function readURL(input) {
    if (input.files && input.files[0]) {
      let reader = new FileReader();

      reader.onload = function(e) {
        let cosa = '#preview-' + $(input).attr('name');
        $(cosa).attr('src', e.target.result);
      };

      reader.readAsDataURL(input.files[0]);
    }
  }

  $("#seccion-img input[type='file']").change(function() {
    readURL(this);
  });

  $('#materia-u').change(function() {
    readURL(this);
    $('#preview-mp').removeClass('is-hidden');
  });

  $('#ambito-u').change(function() {
    readURL(this);
    $('#preview-ap').removeClass('is-hidden');
  });

  // badge a
  $('#aUpload').change(function() {
    readURL(this);
    $('#preview-aU').removeClass('is-hidden');
  });
  // badge b
  $('#bUpload').change(function() {
    readURL(this);
    $('#preview-bU').removeClass('is-hidden');
  });
  // badge c
  $('#cUpload').change(function() {
    readURL(this);
    $('#preview-cU').removeClass('is-hidden');
  });

  $('#id_active_icon').change(function() {
    readURL(this);
    $('#preview-active_icon').removeClass('is-hidden');
  });

  $('#id_completed_icon').change(function() {
    readURL(this);
    $('#preview-completed_icon').removeClass('is-hidden');
  });

  $('img').each(function() {
    //        let this = $this;
    if ($(this).attr('src') == '') {
      //do nothing
    } else {
      $(this).removeClass('is-hidden');
    }
  });
});

$(document).ready(function() {
  $('.selectize-input input[type=text]').attr('maxlength', '20');
  $('.title span').append($('#id_name').val());
});

/**
 * Reviews file size before submit
 * @returns {boolean}
 */
function is_valid_form_images() {
  result = true;
  let inputs = $("form input[type='file']");
  for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].files.length > 0) {
      let image_size = inputs[i].files[0].size / 1024 / 1024;
      if (image_size > 10) {
        swal('Error', 'El archivo seleccionado excede los 10 MB', 'error');
        result = false;
        break;
      }
    }
  }
  return result;
}
