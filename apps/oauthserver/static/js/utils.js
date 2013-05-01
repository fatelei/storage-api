var Utils = {};

Utils.build_data = function () {
    this.csrf_token = csrf;
    this.err_info_ary = ['<div class="alert alert-error">', '</div>'];
    this.good_info_ary = ['<div class="alert alert-success">', '</div>'];
}

Utils.apply_token = function (url) {
    var obj = this;
    var description = document.getElementsByName("description")[0].value;
    if (description.length == 0) {
        obj.show_err_info("You need input some reason");
        return false;
    }    
    if (!this.show_confirm_msg('Are you sure to get access token?')) {
        return false;
    }
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: {'_xsrf': this.csrf_token, 'description': description},
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
        switch (data.info.authorize) {
            case 0: obj.render_table(data); break;
            case 1: obj.render_form(data); break;
            case 2: obj.render_apply(data); break;
        }
        return false;
    });
    return false;
}

Utils.render_table = function (data) {
    var obj = this;
    var html = '';
    if ('msg' in data.info) {
        obj.show_success_info(data.info.msg);
    }
    html += '<table class="table">';
    html += '<thead><tr><th>Key</th><th>Token</th></tr></thead>';
    html += '<tbody><tr><td>' + data.info.key + '</td><td>' + data.info.token + '</td>';
    html += '</tr></tbody></table>';
    $('.authorize').html(html);
}

Utils.render_form = function (data) {
    var html = '';
    var obj = this;
    if ('msg' in data.info) {
        obj.show_err_info(data.info.msg);
    }
    html += '<div class="auth-form">';
    html += '<p>Input Apply Reason & Click Authorize button to auth</p>';
    html += '<form>' + csrf;
    html += '<textarea rows="4" style="width:300px;" name="description"></textarea><br/>';
    html += '<input class="btn btn-primary btn-large" id="apply" type="button" value="Authorize"/>';
    html += '</form></div>';
    $('.authorize').html(html);   
    $('#apply').bind('click', function () {
        obj.build_data();
        obj.apply_token(token);
        return false;
    });
}

Utils.render_apply = function (data) {
    var html = '';
    var obj = this;
    html += '<table class="table">';
    html += '<thead><tr><th>Apply Staus</th></tr></thead>';
    html += '<tbody><tr><td>' + data.info.apply_status + '<td></tr></tbody></table>';
    $('.authorize').html(html);
}

