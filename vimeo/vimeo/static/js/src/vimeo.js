function VimeoBlock(runtime, element) {
    var iframe = $('.vimeo iframe'),
        player = $f(iframe[0])

    function on_finish(id) {
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'mark_as_watched'),
            data: JSON.stringify({watched: true}),
            success: function(result) {
                console.log("watched");
            }
        });
    }

    player.addEvent('ready', function() {
        player.addEvent('finish', on_finish);
    });
}
