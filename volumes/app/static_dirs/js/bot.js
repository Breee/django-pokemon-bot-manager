"use strict";

var start_bot = function() {
    var bot_number = get_bot_number();
    if (bot_number) {
        call_api('up', bot_number);
        setTimeout(function() {
            get_status()
        }, 200);
    }
};

var stop_bot = function() {
    var bot_number = get_bot_number();
    if (bot_number) {
        call_api('down', bot_number);
        setTimeout(function() {
            get_status()
        }, 200);
    }
};

var get_status = function() {
    call_api('status', -1, update_status);
};

var update_status = function(data) {
    $("#bot_status > li").each(function(i) {
        var item = $(this).find('i')[0];
        if (data[i]) {
            $(item).removeClass('fa-times-circle');
            $(item).addClass('fa-check-circle');
        } else {
            $(item).removeClass('fa-check-circle');
            $(item).addClass('fa-times-circle');
        }
    });
};

var show_bot_log = function() {
    var bot_number = get_bot_number();
    if (bot_number) {
        redirect_api('output', bot_number);
    }
};

var clear_bot_log = function() {
    var bot_number = get_bot_number();
    if (bot_number) {
        call_api('output/clear', bot_number);
    }
};

var git_pull = function() {
    var bot_number = get_bot_number();
    if (bot_number) {
        redirect_api('git_pull', bot_number);
    }
};

var get_bot_number = function() {
    var input = $( "#bot_input option:selected" ).val();
    if (input !== "-1") {
        return input;
    }
    else {
        alert('Please select a bot first!');
        return false;
    }
};

var redirect_api = function(fn, bot_number) {
    window.location.href = '/bot/' + fn + "?bot=" + bot_number;
};

var call_api = function (fn, bot_number, success_function) {
    var url = '/bot/' + fn;
    if (bot_number !== -1) {

        url += "?bot=" + bot_number;
    }
    if (success_function === undefined) {
        //TODO error handling
        $.get(url, function (data) {});
    } else {
        $.get(url, function (data) {
            success_function(data);
            }, "json");
    }

};