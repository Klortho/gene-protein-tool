$(document).ready(function() {
  var csrftoken = $.cookie('csrftoken');
  var rsid = $("meta[name=resultset_id]").attr('content');
  var archive = $("meta[name=resultset_archive]").attr('content') == 'True';


  $('#save_button').on('click', function(e) {
    $.post(
      '/save/', 
      {
        'csrfmiddlewaretoken': csrftoken,
        'result_id': rsid
      }, 
      function(r) {
        alert(r);
      }
    )
      .fail(function(err) {
        // FIXME: need a popper here explaining that the save operation failed
        alert(err);
      });
  });
});