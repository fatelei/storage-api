function create_rename_ui() {
    var html = "";
    html += '<div class="modal-header"><button type="button" class="close" data-dismiss="modal">x</button>';
    html += '<h3>文件重命名</h3></div>';
    html += '<div class="modal-body">';
    html += '<form class="form-horizontal" method="POST" action="">';
    html += csrf_token;
    html += '<fieldset>';
    html += '<div class="control-group"><label class="control-label" for="id_new_name">文件名称</label>';
    html += '<div class="controls"><input type="text" id="new_name" name="new_name" maxlength="30"/></div></div>';
    html += '<div class="control-actions"><input type="submit" class="btn btn-primary pull-right" id="rename" value="重命名"/></div>'
    html += '</fieldset></form></div>';
    $('#op-modal').html(html);
}

function rename(rename_url) {
    create_rename_ui();
    $('#new_name').blur(function() {
        clear_attr(this);
        if (this.value.length == 0 || this.value.length > 12) {
            $(this).parent().parent().addClass('error');
            $(this).parent().append('<span class="help-inline">文件名长度不符合要求</span>');
        } else {
            var csrf_token = document.getElementsByName('csrfmiddlewaretoken');
            $.ajax({
                url: check_filename_exist_url,
                type: 'POST',
                dataType: 'json',
                data: {'_xsrf': '', 'new_filename', this.value}
            }).done(function (data) {
                if ('msg' in data && data.errmsg.length != 0) {
                    $('#new_name').parent().parent().addClass('error');
                    $('#new_name').parent().append('<span class="help-inline">' + data.msg + '</span>');
                } else {
                    if (data.exist) {
                        $('#new_name').parent().parent().addClass('error');
                        $('#new_name').parent().append('<span class="help-inline">filename is exists</span>');
                    }
                }
            });
        }
    });
    $('#op-modal').modal('show');
    $('#rename').bind('click', function() {
        if (check_rename() && !$('#new_name').parent().parent().hasClass('error')) {
            start_rename(rename_url);
        }
        return false;
    });
}

function check_rename() {
    var obj = document.getElementsByName('new_name');
    clear_attr(obj);
    if (obj[0].value.length == 0 || obj[0].value.length > 12) {
        $(obj).parent().parent().addClass('error');
        $(obj).parent().append('<span class="help-inline">文件名长度不符合要求</span>');
        return false;
    }
    return true;
}

function start_rename(rename_url) {
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken');
    var obj = document.getElementsByName('new_name');
    clear_attr(obj);
    $.ajax({
        url: '', 
        type: 'POST',
        dataType: 'json',
        data: {'_xsrf': csrf_token[0].value, 'filename': '', 'new_filename': ''}
    }).done(function(data) {
        if ('msg' in data) {
            $(obj).parent().parent().addClass('error');
            $(obj).parent().append('<span class="help-inline">' + data.msg + '</span>');
        } else {
            $('#op-modal').modal('hide');
            alert(data.msg);
        }
        return false;
    });
    return false;
}