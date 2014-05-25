function VimeoEditBlock(runtime, element) {
  $(element).find('.save-button').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
    var data = {
      href: $(element).find('input[name=href]').val(),
      width: $(element).find('input[name=width]').val(),
      height: $(element).find('input[name=height]').val(),
      display_name: $(element).find('input[name=display_name]').val()
    };
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      window.location.reload(false);
    });
  });

  $(element).find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });
}
