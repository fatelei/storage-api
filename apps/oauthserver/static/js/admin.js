PageClick = function (PageClickNum) {
    go_click_page(PageClickNum);
}

function go_click_page(PageClickNum) {
    page.page = PageClickNum;
    render_admin_data();
}

function render_admin_data() {
    var visit_url = data_url + '?offset=' + page.page + '&x=' + Math.random();
    console.log(visit_url);
    $.ajax({
        url: visit_url,
        type: 'GET',
        dataType: 'json',
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(textStatus);
        }
    }).done(function (data) {
        console.log(data);
        page.page = data.page;
        page.totalpage = data.totalpage;
        $(".media-pager").pager({pagenumber: page.page,
                                 pagecount: page.totalpage,
                                 buttonClickCallback: PageClick});
        $('#data-table tbody').html(build_render_data(data.data));
        return false;
    });
    return false;
}


function build_render_data(data) {
    var html = '';
    for (var i = 0; i < data.length; i++) {
        html += '<tr><td>' + data[i].name + '</td>';
        html += '<td>' + data[i].description + '</td>';
        html += '<td>' + data[i].apply_status + '</td>';
        html += '<td><div class="btn-group"><a class="btn dropdown-toggle" data-toggle="dropdown" href="#">';
        html += 'Action<span class="caret"></span></a>';
        html += '<ul class="dropdown-menu">';
        html += generate_action(data[i].status, data[i].member_id);
        html += '</ul></td></tr>';
    }
    return html;
}

function generate_action(status, member_id) {
    var html = '';
    switch (status) {
        case 0:
            html += '<li><a href="#" onclick=\'return admin_action("pass","' + member_id + '");\'>Pass</a></li>';
            html += '<li><a href="#" onclick=\'return admin_action("refuse", "' + member_id + '");\'>Refuse</a></li>';
            break;
        case 1:
            html += '<li><a href="#" onclick=\'return admin_action("refuse", "' + member_id + '");\'>Refuse</a></li>';
            break;
        case 2:
            html += '<li><a href="#" onclick=\'return admin_action("pass","' + member_id + '");\'>Pass</a></li>';
            break;
    }
    return html;
}

function admin_action(action_type, apply_id) {
    var csrf_token = document.getElementsByName('_xsrf')[0].value;
    $.ajax({
        url: data_url,
        type: 'POST',
        dataType: 'json',
        data: {'_xsrf': csrf_token, 'action': action_type, 'member_id': apply_id},
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(textStatus);
        }
    }).done(function (data) {
        console.log(data);
        var msg = '<div class="alert alert-info>' + data.msg + '</div>';
        $('.info-modal .modal-body').html(msg);
        render_admin_data();
        return false;
    });
    return false;
}
