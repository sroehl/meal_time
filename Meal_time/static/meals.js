var index = 1;
$( "#add_ingredient" )
  .click(function (e) {
      e.preventDefault();
      var amount_input = $('<td>').append($('<input>').attr({
            type: 'text',
            id: 'amount_' + index ,
            name: 'amount_' + index
          }));
      var ingredient_input = $('<td>').append($('<input>').attr({
            type: 'text',
            id: 'ingredient_' + index ,
            name: 'ingredient_' + index
          }));
    ($('<tr>').append(amount_input).append(ingredient_input)).appendTo(('#ingredient_table'));
    index++;
  });