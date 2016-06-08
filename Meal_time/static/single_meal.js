$( "#assign" )
  .change(function () {
    if ($( "#assign option:selected" ).val() != 'none'){
        var date = $( "#assign option:selected" ).val();
        var meal_id = $( "#meal_id").html();
        $.ajax({
          url: '/assign_meal',
          data: {"meal_id": meal_id, "date": date},
          type: 'POST'
        });
    }
  });