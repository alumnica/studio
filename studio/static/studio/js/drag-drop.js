$('.item').each(function(){
    var sbjQty = $(this).attr('subject-qty')
    if (sbjQty == 3){
        $(this).addClass('taller')
    } else if (sbjQty == 4){
        $(this).addClass('tallest')
    }
});



initGrid();

function initGrid() {
  var grid = new Muuri('.grid', {
    dragEnabled: true,
    layoutOnInit: true,
  }).on('move', function () {
    saveLayout(grid);
  });
  saveLayout(grid);
}

function serializeLayout(grid) {
  var itemIds = grid.getItems().map(function (item) {
    return item.getElement().getAttribute('pk');
  });
  return JSON.stringify(itemIds);
}

function saveLayout(grid) {
  var layout = serializeLayout(grid);

  $('#order').val(layout);
}

