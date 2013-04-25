var Utils = {};

Utils.build_data = function () {
    this.csrf_token = document.getElementsByName('_xsrf')[0].value;
    this.err_info_ary = ['<div class="alert alert-error">', '</div>'];
    this.good_info_ary = ['<div class="alert alert-success">', '</div>'];
}

Utils.apply_token = function (url) {
    var obj = this;
    if (!this.show_confirm_msg('Are you sure to get access token?')) {
        return false;
    }
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: {'_xsrf': this.csrf_token, 'type': 'add'},
        error: function (jpXHR, textStatus, errorThrown) {
            console.log('apply error: ' + textStatus);
            return false;
        }
    }).done(function (data) {
        if ('errmsg' in data) {
            obj.show_err_info(data.errmsg);
        } else { 
            obj.show_success_info(data.msg);
            obj.render_data(url);
        }
    });
    return false;
}

Utils.update_token = function (url) {
    var obj = this;
    if (!this.show_confirm_msg('Are you sure to update your access token?')) {
        return false;
    }
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: {'_xsrf': this.csrf_token, 'type': 'update'},
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('update error: ' + textStatus);
        }
    }).done(function (data) {
        if ('errmsg' in data) {
            obj.show_err_info(data.errmsg);
        } else {
            obj.show_success_info(data.msg);
            obj.render_data(url);
        }
    });
    return false;
}

Utils.delete_token = function (url) {
    var obj = this;
    if (!this.show_confirm_msg('Are you sure to delete it?')) {
        return false;
    }
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: {'_xsrf': this.csrf_token, 'type': 'delete'},
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('delete token: ' + textStatus);
        }
    }).done(function (data) {
        if ('errmsg' in data) {
            obj.show_err_info(data.errmsg);
        } else {
            obj.show_success_info(data.msg);
            obj.render_data(url);
        }
    });
    return false;
}

Utils.show_confirm_msg = function (msg) {
    if (confirm(msg)) {
        return true;
    } else {
        return false;
    }
}

Utils.show_err_info = function (errmsg) {
    var html = '';
    html += this.err_info_ary[0] + errmsg + this.err_info_ary[1];
    $('#info-modal .modal-body').html(html);
    this.show_info();
}

Utils.show_success_info = function (msg) {
    var html = '';
    html += this.good_info_ary[0] + msg + this.good_info_ary[1];
    $('#info-modal .modal-body').html(html);
    this.show_info();
}

Utils.show_info = function () {
    $('#info-modal').modal();
}

Utils.render_data = function (url) {
    var obj = this;
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(textStatus);
        }
    }).done(function (data) {
        if (data.info.authorize) {
            obj.render_table(data);
        } else {
            obj.render_form(data);
        }
    });
}

Utils.render_table = function (data) {
    var obj = this;
    var html = '';
    html += '<table class="table">';
    html += '<thead><tr><th>Key</th><th>Token</th><th>Left</th><th>Update</th><th>Delete</th></tr></thead>';
    html += '<tbody><tr><td>' + data.info.key + '</td><td>' + data.info.token + '</td>';
    html += '<td>' + data.info.days + '</td>'
    html += '<td><form class="form-inline">' + csrf;
    html += '<button class="btn btn-info" id="update" type="button">Refresh</button></form></td>';
    html += '<td><form class="form-inline">' + csrf;
    html += '<button class="btn btn-info" id="delete" type="button">Delete</button></form></td>';
    html += '<tbody></table>';
    $('.authorize').html(html);
    $('#update').bind('click', function () {
        obj.build_data();
        obj.update_token(token);
        return false;
    });
    $('#delete').bind('click', function () {
        obj.build_data();
        obj.delete_token(token);
        return false;
    });
}

Utils.render_form = function (data) {
    var html = '';
    var obj = this;
    html += '<div class="auth-form">';
    html += '<p>Click Authorize button to auth</p>';
    html += '<form>' + csrf;
    html += '<input class="btn btn-primary btn-large" id="apply" type="button" value="Authorize"/>';
    html += '</form></div>';
    $('.authorize').html(html);   
    $('#apply').bind('click', function () {
        obj.build_data();
        obj.apply_token(token);
        return false;
    });
}

