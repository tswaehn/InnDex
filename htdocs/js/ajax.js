function ajax( cmd, func_callback ){

    jQuery.support.cors = true;
    $.ajax ({
        url: '/api',
        type: 'POST',

        data: JSON.stringify({
                'command':cmd,
                'data':'some data here and there'
                }),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: ajax_response })

    function ajax_response( jsonObj ){

        log = jsonObj['log']
        data = jsonObj['data']

        // execute callback
        func_callback( data, log )
    }
}

