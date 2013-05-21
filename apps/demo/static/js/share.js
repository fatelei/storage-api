function create_share_ui() {
    var html = "";
    html += '<div class="modal-header"><button type="button" class="close" data-dismiss="modal">x</button>';
    html += '<h3>文件分享</h3></div>';
    html += '<div class="modal-body">';
    html += '<form class="form-horizontal" method="POST" action="">';
    html += csrf_token;
    html += '<div class="control-group"><label class="control-label" for="id_username">分享给</label>';
    html += '<div class="controls"><input type="text" data-provide="typeahead" id="username" name="username" maxlength="30"/></div></div>';
    html += '<div class="control-group"><div class="controls">';
    html += '<input type="button" class="btn btn-primary pull-right" id="share_file" value="分享"/></div></div>'
    html += '</form></div>';
    $('#op-modal').html(html);
}

function share(filename) {
    create_share_ui();
    $('#username').blur(function() {
        var value = this.value;
        clear_attr(this);
        if (this.value.length == 0 || this.value.length > 40) {
            $(this).parent().parent().addClass('error');
            $(this).parent().append('<span class="help-inline">不存在此用户</span>');
        }
    });
    $('#op-modal').modal('show');
    get_share_user();
    $('#share_file').bind('click', function() {
        if (check_share_username() && !$('#username').parent().parent().hasClass('error')) {
            start_share(filename);
        }
        return false;
    });
}

function check_share_username() {
    var obj = document.getElementsByName('username');
    clear_attr(obj);
    if (obj[0].value.length == 0 || obj[0].value.length > 40) {
        $(obj).parent().parent().addClass('error');
        $(obj).parent().append('<span class="help-inline">不存在此用户</span>');
        return false;
    }
    return true;
}


function get_share_user() {
    $.ajax({
        url: search_user_url,
        type: 'GET',
        dataType: 'json'
    }).done(function (data) {
        console.log(data);
        $('#username').typeahead({source: data})
    });
}

function start_share(filename) {
    var csrf = document.getElementsByName('_xsrf');
    var obj = document.getElementsByName('username');
    clear_attr(obj);
    $.ajax({
        url: share_url, 
        type: 'POST',
        dataType: 'json',
        data: {'_xsrf': csrf[0].value, 'filename': filename, 'username': obj[0].value}
    }).done(function(data) {
        console.log(data);
        if ('errmsg' in data) {
            $(obj).parent().parent().addClass('error');
            $(obj).parent().append('<span class="help-inline">' + data.errmsg + '</span>');
        } else {
            $('#op-modal').modal('hide');
            alert(data.msg);
            render_user_files();
        }
        return false;
    });
    return false;
}