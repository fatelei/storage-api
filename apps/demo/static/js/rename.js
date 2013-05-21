function create_rename_ui() {
    var html = "";
    html += '<div class="modal-header"><button type="button" class="close" data-dismiss="modal">x</button>';
    html += '<h3>文件重命名</h3></div>';
    html += '<div class="modal-body">';
    html += '<form class="form-horizontal" method="POST" action="">';
    html += csrf_token;
    html += '<div class="control-group"><label class="control-label" for="id_new_name">新文件名</label>';
    html += '<div class="controls"><input type="text" id="new_name" name="new_name" maxlength="30"/></div></div>';
    html += '<div class="control-group"><div class="controls">';
    html += '<input type="submit" class="btn btn-primary pull-right" id="rename" value="重命名"/></div></div>'
    html += '</form></div>';
    $('#op-modal').html(html);
}

function rename(old_filename) {
    create_rename_ui();
    $('#new_name').blur(function() {
        var value = this.value;
        clear_attr(this);
        if (this.value.length == 0 || this.value.length > 12) {
            $(this).parent().parent().addClass('error');
            $(this).parent().append('<span class="help-inline">文件名长度过长</span>');
        } else {
            var csrf = document.getElementsByName('_xsrf');
            $.ajax({
                url: check_filename_exist_url,
                type: 'POST',
                dataType: 'json',
                data: {'_xsrf': csrf[0].value, 'new_filename': value}
            }).done(function (data) {
                if ('errmsg' in data && data.errmsg.length != 0) {
                    $('#new_name').parent().parent().addClass('error');
                    $('#new_name').parent().append('<span class="help-inline">' + data.errmsg + '</span>');
                } else {
                    if (data.exist) {
                        $('#new_name').parent().parent().addClass('error');
                        $('#new_name').parent().append('<span class="help-inline">文件名已经存在</span>');
                    }
                }
            });
        }
    });
    $('#op-modal').modal('show');
    $('#rename').bind('click', function() {
        if (check_rename() && !$('#new_name').parent().parent().hasClass('error')) {
            start_rename(old_filename);
        }
        return false;
    });
}

function check_rename() {
    var obj = document.getElementsByName('new_name');
    clear_attr(obj);
    if (obj[0].value.length == 0 || obj[0].value.length > 12) {
        $(obj).parent().parent().addClass('error');
        $(obj).parent().append('<span class="help-inline">文件名长度过长</span>');
        return false;
    }
    return true;
}

function start_rename(old_filename) {
    var csrf = document.getElementsByName('_xsrf');
    var obj = document.getElementsByName('new_name');
    clear_attr(obj);
    $.ajax({
        url: rename_url, 
        type: 'POST',
        dataType: 'json',
        data: {'_xsrf': csrf[0].value, 'filename': old_filename, 'new_filename': obj[0].value}
    }).done(function(data) {
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