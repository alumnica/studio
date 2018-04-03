// import 'taggle';

import $ from 'jquery';
import whatInput from 'what-input';


window.$ = $;


// import 'jquery-ui/ui/core';
import 'jquery-ui/ui/widgets/sortable';
import 'jquery-ui/ui/effects/effect-bounce';


import Foundation from 'foundation-sites';
// If you want to pick and choose which modules to include, comment out the above and uncomment
// the line below
//import './lib/foundation-explicit-pieces';

//Datatables
import 'datatables.net-zf';
import 'datatables.net-responsive-zf';

//Sweet Alert 2

import swal from 'sweetalert2';

window.swal = swal;

//selectize

import 'selectize';

// import './lib/jquery.uploadPreview';

$(document).foundation();


$('#tabla-ambitos').DataTable({
    responsive: true,
    "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
    },
    "columnDefs": [
        { "orderable": false, "targets": [2, 3, 4] }
    ],

});

$('#tabla-materias').DataTable({
    responsive: true,
    "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
    },
    "columnDefs": [
        { "orderable": false, "targets": [2] }
    ],

});



$("#fileUpload").on('change', function () {

    if (typeof (FileReader) != "undefined") {

        var image_holder = $("#image-holder");
        image_holder.empty();

        var reader = new FileReader();
        reader.onload = function (e) {
            $("<img />", {
                "src": e.target.result,
                "class": "thumb-image"
            }).appendTo(image_holder);

        }
        image_holder.show();
        reader.readAsDataURL($(this)[0].files[0]);
    } else {
        alert("This browser does not support FileReader.");
    }
});

$('#changedtext').keyup(function () {
    var textToChange = $(this).val();
    $('.ttc2').text(textToChange);
});

$('#color-button input[type=radio]').click(function () {
    let $this = $(this);
    $('#image-holder').attr('class', $this.data('a'));
    $('#ttc').attr('class', $this.data('b'));
});

//Sortable Materias en creacion de  Ambitos

$(function () {
    $("#sortable").sortable();
    // $( "#sortable" ).disableSelection();
    // deprecated
});


$("#sortable").on('click', '.remove_materia', function () {
    $(this).parent().remove(); 
});

var numMateria = 1;

$("#class-adder").click(function (e) {
    e.preventDefault();
    var text = $("select[name='materias-select']").val();
    
    $("#sortable").append('<li id="mat_'+ numMateria++ +'" class="ui-state-default"><span class="ui-icon ui-icon-arrowthick-2-n-s sorter"></span>' + text + '<span class="remove_materia"><a href="#"><i class="fas fa-minus-square"></i></a></span></li>');
    $("#sortable").sortable('refresh');
});

$('form#ambito-creation').submit(function(){
    
    var texts = [];

    $(function() {
        $('#sortable li').each(function(){
            texts.push($(this).text());
        });

        // alert(texts);
        $('#class_name').val(texts);
    });

    // 

//    return false
//      used to stop POST
}); 

// nav on click

// $("#dash-nav").click(function(){
//     $(this).addClass("is-active");
//     $("#ambito-nav")
// });

{/* <script>
$(function(){
$('#materia-nav').addClass('is-active');
});
</script> */}
