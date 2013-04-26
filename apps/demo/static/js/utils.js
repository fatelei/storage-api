var Utils = function () {
    this.csrf_token = document.getElementsByName("_xsrf")[0].value;
    this.err_info_ary = ['<div class="alert alert-error">', '</div>'];
    this.good_info_ary = ['<div class="alert alert-success">', '</div>'];
    this.page = 0;
    this.totalpage = 0;
    var that = this;

    this.pageclick = function (pageclicknumber) {
        that.go_click_page(pageclicknumber);
    };

    this.go_click_page = function (pageclicknumber) {
        that.page = pageclicknumber;
        that.get_files(page);
    };

    this.get_files = function (page) {
        
    };
    this.download_files = function (url, filenames) {

    };
    this.remove_files = function (url, filenames) {

    };
    this.rename_file = function (url, data) {

    };
    this.upload_file = function (url, data) {

    };
    this.render_table = function (data) {

    };
};
