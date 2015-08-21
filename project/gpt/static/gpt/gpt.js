$(document).ready(function() {
  var csrftoken = $.cookie('csrftoken');
  var rsid = $("meta[name=resultset_id]").attr('content');
  var archived = $("meta[name=resultset_archived]").attr('content') == 'True';

  function saved() {
    $('#save_button').val("Saved")
                     .prop("disabled", true);
  }
  if (archived) saved();


  $('#save_button').on('click', function(e) {
    $.post(
      '/save/', 
      {
        'csrfmiddlewaretoken': csrftoken,
        'resultset_id': rsid
      }, 
      function(r) {
        saved();
      }
    )
      .fail(function(err) {
        alert("Sorry! The save operation failed:\n\n" + 
              err.statusText + "\n" + err.responseText);
      });
  });


  $('.collapse-button')
    .data('collapsed', true)
    .on('click', function(e) {
      var collapsed = $(this).data('collapsed');
      var tbody = $(this).closest('table').find('tbody');
      if (collapsed) {
        tbody.show(200);
      }
      else {
        tbody.hide(200);
      }
      $(this).text(collapsed ? '-' : '+')
             .data('collapsed', !collapsed);
      return false;
    });
});