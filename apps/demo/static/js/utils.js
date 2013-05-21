var handle_check_filename = [];

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
        display_usage();
        return false;
    });
    return false;
}

function render_files (data) {
    var html = '';
    for (var i = 0; i < data.length; i++) {
        html += '<div class="accordion-group"><div class="accordion-heading">';
        html += '<input type="checkbox" onchange="handle_change(this);" name="check_file" value="' + data[i].filename + '"/>';
        html += '<a href="' + download_url + data[i].filename + '">';
        html += '<i class="icon-file"></i>' + data[i].filename + '</a>';
        html += '<a class="accordion-toggle pull-right" \
                 data-toggle="collapse" data-parent="#media-accordion" href="#media' + i + '">更多操作</a>';
        html += '<span class="media-date"><strong>' + data[i].time + '</strong></span>';
        html += '<span class="media-size"><strong>' + data[i].type + '</strong></span></div>';
        html += '<div id="media' + i + '" class="accordion-body collapse">';
        html += '<div class="accordion-inner"><ul class="media-op">';
        html += '<li><i class="icon-download"></i><a href="' + download_url + data[i].filename + '">下载文件</a></li>';
        html += '<li><i class="icon-pencil"></i><a href="#" onclick=\'return rename("' + data[i].filename + '");\'>重命名</a></li>';
        html += '<li class="media-divider"></li>';
        html += '<li><i class="icon-trash"></i><a href="#" onclick=\'return remove_file("' + data[i].filename + '");\'>删除</a></li>';
        html += '<li><i class="icon-share"></i><a href="#" onclick=\'return share("' + data[i].filename + '");\'>文件分享</a></li></ul>';
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

function clear_attr(obj) {
    $(obj).parent().parent().removeClass('error');
    $($(obj).parent().children()[1]).remove();
}

function remove_file(filenames) {
    if (!confirm("你确定要删除所选文件吗?")) {
        return false;
    }
    var csrf = document.getElementsByName("_xsrf");
    $.ajax({
        url: remove_url,
        type: 'POST',
        dataType: 'json',
        data: {"_xsrf": csrf[0].value, "filenames": filenames},
        error: function (jpXHR, textStatus, errorThrown) {
            console.log(textStatus);
            return false;
        }
    }).done(function (data) {
        if ('errmsg' in data) {
            alert(data.errmsg);
        } else {
            alert(data.msg);
            render_user_files();
        }
        return false;
    });
    return false;
}

function remove_batch() {
    var checklists = document.getElementsByName("check_file");
    var filenames = '';
    var length = checklists.length;
    for (var i = 0; i < length - 1; i++) {
        if (checklists[i].checked) {
            filenames += checklists[i].value + ',';
        }
    }
    if (checklists[length - 1].checked) {
        filenames += checklists[length - 1].value;
    }
    if (filenames.length == 0) {
        alert("请选择要删除的文件!");
        return false;
    } else {
        return remove_file(filenames);
    }
}

function handle_change(obj) {
    if (obj.checked) {
        handle_check_filename.push(obj.value);
    } else {
        index = handle_check_filename.indexOf(obj.value);
        handle_check_filename.pop(index);    
    }
    var href = handle_check_filename.join(",");
    href = download_url + href;
    $('#download').attr("href", href);
}

function display_usage() {
    $.ajax({
        url: space_url,
        type: 'GET',
        dataType: 'json',
        error: function (jpXHR, textStatus, errorThrown) {
            console.log(textStatus);
            return false;
        }
    }).done(function (data) {
        if ('errmsg' in data) {
            alert(data.errmsg);
        } else {
            $('#space')[0].innerText = '容量:' + data.usage + '/' + data.capacity/1024/1024 + 'MB';
        }
        return false;
    });
    return false;
}