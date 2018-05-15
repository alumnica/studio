// <!-- Example of JavaScript options for PHP server side -->

$('document').ready(function(){
    var $list = $('#demo .list')
         ,template = Handlebars.compile($('#jplist-template').html());

   $('#demo').jplist({

      itemsBox: '.list'
      ,itemPath: '.list-item'
      ,panelPath: '.w-panel'
       ,debug: true
       ,storageName: 'jplist'
      //data source
      ,dataSource: {

           type: 'server'
           , server: {

               //jQuery ajax settings
               ajax: {
                   url: 'http://localhost:8000/api/images/'
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
