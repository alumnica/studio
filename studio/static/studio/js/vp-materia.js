$(document).ready(function () {

    $('.block').each(function () {

        var theState = $(this).attr('state');
        $(this).addClass(theState);

        var attr = $(this).attr('data-n');

        // For some browsers, `attr` is undefined; for others,
        // `attr` is false.  Check for both.
        if (typeof attr !== typeof undefined && attr !== false) {

            //append to section if already has data-n
            var theBlocknum = $(this).attr('data-n');
            var theBlock = $('#' + theBlocknum);
            $(this).appendTo(theBlock);
        }
    });

    $('.block').on('click', function(e){
        e.stopPropagation(); // <--------------stop here
        $('.thetip').fadeOut(200);
        $('.thetip', this).fadeToggle('150');
    });
    $(document).click(function () { // you don't need the else part to fadeout
      var $el = $(".thetip");
      if ($el.is(":visible")) {
          $el.fadeOut(200);
      }
   });


});