// <!-- Example of JavaScript options for PHP server side -->

$('document').ready(function(){
    var $list = $('#img-jplist .list')
         ,template = Handlebars.compile($('#jplist-template').html());

   $('#img-jplist').jplist({

      itemsBox: '.list'
      ,itemPath: '.img-box'
      ,panelPath: '.filter-panel'
//      ,redrawCallback: function(collection, $dataview, statuses){
//        fill();
//       }

      //data source
      ,dataSource: {

           type: 'server'
           , server: {

               //jQuery ajax settings
               ajax: {
                   url: '/api/images/'
                   , dataType: 'json'
                   , type: 'GET'
                   ,contentType: 'application/json'
               }

           }
           ,render: function (dataItem, statuses) {
            $list.html(template(dataItem.content));
           }

       }
   });


//   var date = $('.date_field');
//   date = date.substring(0,10);
//   $('.date_field').text(date);

});

$( document ).ajaxComplete(function() {
    $('.date_field').each(function () {
        var dateLong = $(this).text();
        date = dateLong.substring(0,10);
        $(this).text(date);
    });

    $('.img-box .file_field').each(function(){

        /*var fileName = fullPath.replace(/^.*[\\\/]/, '');
        $(this).text(fileName);*/

        var checker = $(this).closest('.img-box').find('.deleter');

        $(checker).attr('data-name', $('.file_name_field').text());

    });

    $('.img-box .complete_file').each(function(){
        var checker = $(this).closest('.img-box').find('.deleter');
        $(checker).val($(this).text())
    });

    $('.folder_field').each(function(){
        if ($(this).text()=='ambits') {
            $(this).text('\xC1mbitos')
        } else if ($(this).text()=='subjects'){
            $(this).text('Materias')
        }
    });


    $('.img-box').on('click', '.image', function(){
        var imageUrl = $('.file_field', this).text();
        $('#imgModal img').attr('src', imageUrl);
        $('#dloadBtn').attr('href', imageUrl);

        var theName = $('.file_name_field', this).text();
        $('#nombre').html('<strong>Nombre:</strong> '+theName);

        var theDate = $('.date_field', this).text();
        $('#fecha').html('<strong>Fecha:</strong> '+theDate);

        var attachedTo = $('.name_field', this).text();
        attachedTo = attachedTo.substring(0, attachedTo.indexOf('-'));
        $('#adjuntoa').html('<strong>Adjunto a:</strong> '+attachedTo);


    });


    $('#deleterBtn').on('mouseenter mouseleave', function () {

        var texts = [];
        var names = [];

        $(function () {
            $("input:checkbox[name=deleter]:checked").each(function(){
                texts.push($(this).val());
                names.push($(this).data('name'));
            });

            // alert(texts);
            $('#toBeDeleted').val(texts);
            $('#theNames').val(names);



            var str = '<ul>'

            names.forEach(function(slide) {
              str += '<li>'+ slide + '</li>';
            });

            str += '</ul>';
            document.getElementById("deleteList").innerHTML = str;
        });



    });

    $(function()
    {
      $('[name="deleter"]').change(function()
      {
        if ($(this).is(':checked')) {
           // Do something...
           $('#deleterBtn').prop("disabled", false);
        } else {
           $('#deleterBtn').prop("disabled", true) ;
        };
      });
    });



});



