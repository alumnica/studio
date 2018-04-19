

$(document).ready(function () {

var startPos = null;

interact('.block')
    .draggable({
        // enable inertial throwing
        inertia: true,
		// keep the element within the area of it's parent
        // restrict: {
        //     restriction: "parent",
        //     endOnly: true,
        //     elementRect: { top: 0, left: 0, bottom: 1, right: 1 }
        // },
        snap:{
			targets: [startPos],
            range: Infinity,
            relativePoints: [ { x: 0.5, y: 0.5 } ],
            endOnly: true 
		},
        onmove: dragMoveListener,
        onstart: function (event) {
            
                var rect = interact.getElementRect(event.target);
            
                // record center point when starting the very first a drag
                var startPos = {
                        x: rect.left + rect.width  / 2,
                        y: rect.top  + rect.height / 2
                    }
                
                    event.interactable.draggable({
                snap: {
                        targets: [startPos]
                    }
                });
            },
       
		
    });

 function dragMoveListener (event) {
    var target = event.target,
        // keep the dragged position in the data-x/data-y attributes
        x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx,
        y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

    // translate the element
    target.style.webkitTransform =
    target.style.transform =
      'translate(' + x + 'px, ' + y + 'px)';

    // update the posiion attributes
    target.setAttribute('data-x', x);
    target.setAttribute('data-y', y);
  };

  function revertBack(event) {
    var target = event.target;
    target.style.webkitTransform =
    target.style.transform =
    'translate(0px, 0px)';

    target.setAttribute('data-x', 0);
    target.setAttribute('data-y', 0);
};


  interact('.dropzone').dropzone({
    // enable draggables to be dropped into this
    // overlap: 'center',
    // only accept elements matching this CSS selector
    // accept: '.block',

    ondragenter: function (event) {
        var draggableElement = event.relatedTarget,
            dropzoneElement = event.target,
            dropRect = interact.getElementRect(dropzoneElement),
		    dropCenter = {
                x: dropRect.left + dropRect.width  / 2,
                y: dropRect.top  + dropRect.height / 2
		    };

		event.draggable.draggable({
            snap: {
                targets: [ dropCenter ]
            }
		});


        // feedback the possibility of a drop
        dropzoneElement.classList.add('drop-target');
        draggableElement.classList.add('can-drop');
    },
    ondragleave: function (event) {
		// when leaving a dropzone, snap to the start position
		
		event.draggable.draggable({
            snap: {
                targets: [ startPos ]
            }
		});

		// remove the drop feedback style
        event.target.classList.remove('drop-target');
        event.relatedTarget.classList.remove('can-drop');
    },
    ondropactivate: function (event) {
        // add active dropzone feedback
        event.target.classList.add('drop-active');
    },
    ondropdeactivate: function (event) {
        // remove active dropzone feedback
        event.target.classList.remove('drop-active');
        event.target.classList.remove('drop-target');
    },
    ondrop: function (event) {
            // add data-n of target
        event.relatedTarget.setAttribute('data-n', event.target.id)
		// in all the hidden inputs place the id of target in value
        $(function () {
            var i = 1;
            $('.block').each(function(){			
                $('#p-block-'+i).val(this.getAttribute('data-n'));	
            i++;			
            });
        });
    }
  });
});

$(document).ready(function () {
    var i = 0
    $('.block').each(function () {
        i++;
        $('#inputs-h').prepend(
            $('<input>').attr({
                type: 'hidden',
                id: 'p-block-' + i,
                name: 'p-block-' + i,
            })
        );
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
});