// <!-- Example of JavaScript options for PHP server side -->

$('document').ready(function () {
    var $list = $('#img-jplist .list')
        , template = Handlebars.compile($('#jplist-template').html());

    $('#delete_images').on('click', function () {
        let urls = $('#toBeDeleted').val();
        let urls_array = urls.split(',');

        for (let i = 0; i < urls_array.length; i++) {
            delete_article(urls_array[i]);
        }
    });

    function delete_article(url) {
        $.ajax({
            url: url,
            data: url,
            type: "DELETE",
            success: function (son) {
                console.log("delete successful")
            }
        })
    }

    $('#img-jplist').jplist({

        itemsBox: '.list'
        , itemPath: '.img-box'
        , panelPath: '.filter-panel'
//      ,redrawCallback: function(collection, $dataview, statuses){
//        fill();
//       }

        //data source
        , dataSource: {

            type: 'server'
            , server: {

                //jQuery ajax settings
                ajax: {
                    url: '/api/images/'
                    , dataType: 'json'
                    , type: 'GET'
                    , contentType: 'application/json'
                }

            }
            , render: function (dataItem, statuses) {
                $list.html(template(dataItem.content));
            }

        }
    });


//   var date = $('.date);
//   date = date.substring(0,10);
//   $('.date).text(date);

});

$(document).ajaxComplete(function () {
    $('.date').each(function () {
    var dateLong = $(this).text();
    date = dateLong.substring(0, 10);
    $(this).text(date);
});

$('.img-box .file).each(function(){

/*var fileName = fullPath.replace(/^.*[\\\/]/, '');
$(this).text(fileName);*/

var checker = $(this).closest('.img-box').find('.deleter');

$(checker).attr('data-name', $('.file_name').text());

})
;

$('.img-box .complete_file').each(function () {
    var checker = $(this).closest('.img-box').find('.deleter');
    $(checker).val($(this).text())
});

$('.folder').each(function(){
if ($(this).text() == 'ambits') {
    $(this).text('\xC1mbitos')
} else if ($(this).text() == 'subjects') {
    $(this).text('Materias')
}
})
;


$('.img-box').on('click', '.image', function () {
    var imageUrl = $('.file', this).text();
    $('#imgModal img').attr('src', imageUrl);
    $('#dloadBtn').attr('href', imageUrl);

    var theName = $('.file_name', this).text();
    $('#nombre').html('<strong>Nombre:</strong> ' + theName);

    var theDate = $('.date', this).text();
    $('#fecha').html('<strong>Fecha:</strong> ' + theDate);

    var attachedTo = $('.name', this).text();
    attachedTo = attachedTo.substring(0, attachedTo.indexOf('-'));
    $('#adjuntoa').html('<strong>Adjunto a:</strong> ' + attachedTo);


});


$('#deleterBtn').on('mouseenter mouseleave', function () {

    var texts = [];
    var names = [];

    $(function () {
        $("input:checkbox[name=deleter]:checked").each(function () {
            texts.push($(this).val());
            names.push($(this).data('name'));
        });

        // alert(texts);
        $('#toBeDeleted').val(texts);
        $('#theNames').val(names);


        var str = '<ul>'

        names.forEach(function (slide) {
            str += '<li>' + slide + '</li>';
        });

        str += '</ul>';
        document.getElementById("deleteList").innerHTML = str;
    });


});

$(function () {
    $('[name="deleter"]').change(function () {
        if ($(this).is(':checked')) {
            // Do something...
            $('#deleterBtn').prop("disabled", false);
        } else {
            $('#deleterBtn').prop("disabled", true);
        }
        ;
    });
});

})
;



