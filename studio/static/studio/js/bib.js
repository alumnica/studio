// <!-- Example of JavaScript options for PHP server side -->

$('document').ready(function(){
    var $list = $('#img-jplist .list')
         ,template = Handlebars.compile($('#jplist-template').html());

   $('#img-jplist').jplist({

      itemsBox: '.list'
      ,itemPath: '.img-box'
      ,panelPath: '.jplist-panel'
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

});
