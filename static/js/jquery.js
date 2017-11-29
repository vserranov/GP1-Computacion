$(function() {
  $('input').click(function() {
    var local = $('#MediaLocal').val();
    var remota = $('#MediaRemota').val();
    $.ajax({
      url: '/media',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
        console.log(response);
      },
      error: function(error) {
        console.log(error);
      }
    });
  });
});


$(document).ready(function(){
  var clicked;
  $(".favorite").click(function(){
    clicked = $(this).attr("name");
    $.ajax({
      type : 'POST',
      url : "{{url_for('media')}}",
      contentType: 'application/json;charset=UTF-8',
      data : {'data':clicked}
    });
  });
});
