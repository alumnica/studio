$(document).ready(function () {
    $(".block").draggable({
        revert: "invalid",
        // cursor: "grab",
        containment: '#ovc',
        // snap: '#dpp',
        // snapMode: "inner",
        // snapTolerance: 50,
        helper: "clone",
    });

    $(".dropzone").droppable({
        activeClass: "dropOn",
        hoverClass: "drop-hover",
        accept: ".block",
        drop: function (event, ui) {
            var theDrag = ui.draggable;
            theDrag.children('.return-button').remove();
            ui.draggable.detach().appendTo($(this));
            var blockId = ui.draggable.attr("id"),
                blockId = blockId.split("-").pop();
            var closBtnContent = ('<div class="return-button" block-val="ob-' + blockId + '"><i class="fa fa-times"></i></div>')

            ui.draggable.append(closBtnContent);
            $(this).droppable('option', 'accept', ui.draggable);

            var dropCoor = $(this).attr('id');
            ui.draggable.attr('data-n', dropCoor);
        },
        out: function (event, ui) {
            $(this).droppable('option', 'accept', '.block');
        }
    });
    //copy to shadow block
    $('.oda-block').each(function () {
        var shadowContent = $('.block', this).html();
        $('.shadow-block', this).append(shadowContent);

    })
    $('.block').each(function () {
        var attr = $(this).attr('data-n');

        // For some browsers, `attr` is undefined; for others,
        // `attr` is false.  Check for both.
        if (typeof attr !== typeof undefined && attr !== false) {
            //return button
            var blockId = $(this).attr("id"),
                blockId = blockId.split("-").pop();
            var closBtnContent = ('<div class="return-button" block-val="ob-' + blockId + '"><i class="fa fa-times"></i></div>')
            $(this).append(closBtnContent);
            //append to section if already has data-n
            var theBlocknum = $(this).attr('data-n');
            var theBlock = $('#' + theBlocknum);
            $(this).appendTo(theBlock);
            theBlock.droppable('option', "disabled", true);
            $(this).on("mousedown", function () {
                theBlock.droppable("option", "disabled", false);
            });
        }
    });
    $('.block').on('click', '.return-button', function(){
        var sendId = $(this).parent().attr('id').split("-").pop();
		// $(this).parent().parent().droppable("option", "disabled", false);
		$(this).parent().parent().droppable('option', 'accept', '.block');
        $(this).parent().appendTo('#ob-'+sendId);
        $(this).remove();
    });
    
    $('#psBtn').on('mouseover', function(){
        var posTotal = '';
        $('#oda-position').val(posTotal)
        $('.dropzone').each(function(){
            if ( $(this).children().length > 0 ) {                
                var blockNum = $(this).children().attr('id').split("-").pop();
                var dropNum = $(this).children().attr('data-n');
                var posTotal = (blockNum+','+dropNum);
                if ($('#oda-position').val()=='') {
                    $('#oda-position').val(posTotal)
                } else {
                    $('#oda-position').val(posTotal+';'+$('#oda-position').val());
                }
           }
        });
    });
    
});

$(document).ready(function () {
	
	$("#section-1 img").each(function(){
		$(this).appendTo("#"+(this.getAttribute('data-n')));
    });
    
    $("#section-2 img").each(function(){
		$(this).appendTo("#"+(this.getAttribute('data-n')));
    });
    
    $("#section-3 img").each(function(){
		$(this).appendTo("#"+(this.getAttribute('data-n')));
	});

	$("#section-4 img").each(function(){
		$(this).appendTo("#"+(this.getAttribute('data-n')));
	});
});