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


function upload_files() {
    var $file = $('#uploadFile');
    var $form = $('#upload_file_form');
    var $progress = $('.bar');
    var up = new uploader($file.get(0),
                          $form.get(0),
                            {
                                multiple: true,
                                url: files_upload_url,
                                progress: function (ev) {
                                    console.log('progress');
                                    $progress.css('width', ((ev.loaded/ev.total)*100+'%'));
                                },
                                error: function (ev) {
                                    $('#load-modal').modal('hide');
                                    console.log('error');
                                },
                                success: function (ev) {
                                    $('#upload-modal').modal('hide');
                                    $('#load-modal').modal('hide');
                                    render_user_files();
                                    console.log('success');   
                                }
                            }
    );
    $('#load-modal').modal();
    up.send();
    return false;
}

function remove_files() {

    return false;
}

function download_files() {
    
    return false;
}
