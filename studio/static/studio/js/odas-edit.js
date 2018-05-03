//More (Expand) or Less (Collapse)
$('.oda-materias').each(function(){
    var filterAmount = $(this).find('li').length;
    if( filterAmount > 5){    
      $('li', this).eq(4).nextAll().hide().addClass('toggleable');
      $(this).append('<li class="more">Más &darr;</li>');    
    }  
  });
  
  $('.oda-materias').on('click','.more', function(){
    if( $(this).hasClass('less') ){    
      $(this).text('Más \u2193').removeClass('less');    
    }else{
      $(this).text('Menos \u2191').addClass('less'); 
    }
    $(this).siblings('li.toggleable').slideToggle(); 
  }); 


var sinMomentos = 0;

$('.activity-num').each(function () {
    var x = $(this).text()
    if (x == 0) {
        $(this).find('span').html('<i class="fas fa-times"></i>');
        sinMomentos++;
        $(this).addClass('noMom');
    } else {
        $(this).find('span').html('<i class="fas fa-check"></i>');
    };
});

$('#sinMomentos').find('span').html(sinMomentos);


$('document').ready(function(){
        
    $('#odaSortList').jplist({				
        itemsBox: '.odas-list', 
        itemPath: '.oda-container', 
        panelPath: '.jplist-panel'	
    });  
    
});


$('.assigned-to_materias li').each(function() {
        var theClass = $(this).text().replace(/\s/g,"-");
        
       $(this).addClass(theClass); 
});

$('.oda-tags li').each(function(){
        var theClass = $(this).text().replace(/\s/g,"-");        
       $(this).addClass(theClass); 
});
    


$('.oda-materias li').each(function(){
	var subjectName = $(this).text().replace(/\s/g,"-");
	var classQuantity = $('.'+ subjectName).length;
  $(this).find('span').text(classQuantity);
});

var noMat = 0

$('.assigned-to_materias').each(function(){
	if ($(this).has('li').length == 0) {
        $(this).addClass('noMat');
        noMat++;
    }
});

$('#sinMateria').find('span').html(noMat);

$('.oda-tags-list li').each(function(){
	var tagName = $(this).text().replace(/\s/g,"-");
	$(this).attr({
		"data-control-type":"button-filter",
		"data-control-action":"filter",
        "data-selected":" false",
        "data-control-name": tagName,
        "data-path":"."+tagName,		
	})
});

$.fn.ignore = function(sel){
    return this.clone().find(sel||">*").remove().end();
  };

$('.oda-materias li').each(function(){
	var matName =$(this).ignore("span").text().replace(/\s/g,"-");
	$(this).attr({
		"data-control-type":"button-filter",
		"data-control-action":"filter",
        "data-selected":" false",
        "data-control-name": matName,
        "data-path":"."+matName,		
	})
});
