PageClick = function (click_num) {
    go_to_click_page(click_num);
}

function go_to_click_page (click_num) {
    page.page = click_num;
    render_user_files();
}

function render_user_files () {
    var visit_url = files_url + '?offset=' + page.page + '&x=' + Math.random();
    $.ajax({
        url: visit_url,
        type: 'GET',
        dataType: 'json',
        error: function (jpXHR, textStatus, errorThrown) {
            console.log(textStatus);
            return false;
        }
    }).done(function (data) {
        console.log(data);
        page.page = data.page;
        page.totalpage = data.totalpage;
        $(".media-pager").pager({pagenumber: page.page,
                                 pagecount: page.totalpage,
                                 buttonClickCallback: PageClick});
        $('#media-accordion').html(render_files(data.data));
        return false;
    });
    return false;
}

function render_files (data) {
    var html = '';
    for (var i = 0; i < data.length; i++) {
        html += '<div class="accordion-group"><div class="accordion-heading">';
        html += '<a href="#">';
        html += '<i class="icon-file"></i>' + data[i].filename + '</a>';
        html += '<a class="accordion-toggle pull-right" \
                 data-toggle="collapse" data-parent="#media-accordion" href="#media' + i + '">更多操作</a>';
        html += '<span class="media-date"><strong>' + data[i].time + '</strong></span>';
        html += '<span class="media-size"><strong>' + data[i].type + '</strong></span></div>';
        html += '<div class="accordion-inner"><ul class="media-op">';
        html += '<li><i class="icon-download"></i><a href="#">Download</a></li>';
        html += '<li><i class="icon-pencil"></i><a href="#">Rename</a></li>'
        html += '<li class="media-divider"></li>';
        html += '<li><i class="icon-trash"></i><a href="#">Remove</a></li></ul>';
        html += '</div></div></div>';
    }
    return html;
}


function upload_file() {
    var files = document.getElementByNames('upload_file')[0].files;
    if (files) {
        for (var i = files.length; i++) {
            start_send_data(files[i]);
        }
    }
    return false;
}

function start_send_data(file) {
    var reader = new FileReader();
    reader.readAsText(file, "utf-8");
    reader.onprogress = update_progress;
    reader.onload = loaded;
    reader.onerror = upload_error;
}

function update_progress(evt) {
    if (evt.lengthComputable) {
        var loaded = (evt.loaded / evt.total);
        if (loaded < 1) {

        }
    }
}

function loaded(evt) {
    var filestring = evt.target.result;
    console.log(evt.target);
}