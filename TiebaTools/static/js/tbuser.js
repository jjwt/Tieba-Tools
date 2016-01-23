var CURRENT_TBUID = null;
var PN_TBUSER_LIST = 1;
function tbuser_list() {
    $("#message").html("正在获取贴吧用户列表...");
    $(document).ready(function(){
        $.ajax({
            url:"/tbuser/get",
            async:true,
            dataType:"json",
            type:'POST',
            data:{
                'pn': PN_TBUSER_LIST
            },
            complete: function(x,y) {
                ;
            },
            success: function(x) {
                $("#message").html("");
                return parse_tbuserlist(x);
            },
            error: function(x) {
                $("#message").html("操作失败，发生未知错误!");
            }
        });
    });
    return false;
}

function parse_tbuserlist(jsn) {
    var s='';
    if (jsn["count_tbusers"].length == 0) {
        s+=[
            "你还没绑定贴吧用户，请前往",
            '<a href="#" onclick="return tbuser_add_get();">绑定</a>'
        ].join('');
        $("#content").html(s);
        return false;
    }
    if (CURRENT_TBUID==null) {
        CURRENT_TBUID = jsn["tbusers"][0]["id"];
    }
    s += [
        '<div class="panel panel-primary">',
            '<div class="panel-heading">',
                '共绑定'+jsn["count_tbusers"]+'个贴吧用户。',
            '</div>',
            '<table class="table">',
                '<thead>',
                    '<tr>',
                        '<th>#</th>',
                        '<th>贴吧用户名</th>',
                        '<th>操作</th>',
                    '</tr>',
                '</thead>',
                '<tbody>',
    ].join('');
    for (var i=0; i < jsn["tbusers"].length; ++i) {
        s += [
                '<tr>',
                    '<th scope="row">'+ ((jsn["pn_tbusers"]-1)*jsn["num_per_tbusers"]+i+1)+'</th>',
                    '<td>'+jsn["tbusers"][i]["tbuser_name"]+'</td>',
                    '<td> <a href="/" tbuid="' + jsn["tbusers"][i]["id"] + '" onclick="return tbuser_del(this);">解绑</a></td>',
                    jsn["tbusers"][i]["id"] == CURRENT_TBUID ? '<td>当前用户</td>': '<td> <a href="/" tbuid="' + jsn["tbusers"][i]["id"] + '" onclick="return tbuser_del(this);">置为当前</a></td>',
                '</tr>',
        ].join('');
    }
    s += [
                '</tbody>',
            '</table>',
            gen_pagernav(PN_TBUSER_LIST, jsn["max_pn_tbusers"], "PN_TBUSER_LIST", "return tbuser_list()"),
        '</div>'
    ].join('');
    $("#content").html(s);
    return false;
}

//deprecated
function parse_tbuserlist2(jsn) {
    var s='';
    if (jsn["count_tbusers"].length == 0) {
        s+=[
            "你还没绑定贴吧用户，请前往",
            '<a href="#" onclick="return tbuser_add_get();">绑定</a>'
        ].join('');
        $("#content").html(s);
        return false;
    }
    s += [
        '<div class="panel panel-primary">',
        '<div class="panel-heading">',
        '共绑定'+jsn["count_tbusers"]+'个贴吧用户。',
        '</div>',
        '<table class="table">',
            '<thead>',
                '<tr>',
                    '<th>#</th>',
                    '<th>贴吧用户名</th>',
                    '<th>操作</th>',
                '</tr>',
            '</thead>',
            '<tbody>',
    ].join('');
    for (var i=0; i < jsn["tbusers"].length; ++i) {
        s += [
                '<tr>',
                    '<th scope="row">'+ ((jsn["pn_tbusers"]-1)*jsn["num_per_tbusers"]+i+1)+'</th>',
                    '<td>'+jsn["tbusers"][i]["tbuser_name"]+'</td>',
                    '<td> <a href="/" tbuid="' + jsn["tbusers"][i]["id"] + '" onclick="return tbuser_del(this);">解绑</a></td>',
                    '<td> <a href="/" tbuid="' + jsn["tbusers"][i]["id"] + '" onclick="return tbuser_del(this);">置为当前</a></td>',
                '</tr>',
        ].join('');
    }
    s += [
                '</tbody>',
            '</table>',
        '<nav>',
            '<ul class="pager">',
                '<li ',
                PN_TBUSER_LIST < 2 ? 'class="disabled"' : '',
                '>',
                    '<a href="#" arial-label="First" onclick="PN_TBUSER_LIST=1;return tbuser_list();">',
                        '<span class="glyphicon glyphicon-step-backward"',
                              'arial-hidden="true"></span>',
                    '</a>',
                '</li>',
                '<li ',
                PN_TBUSER_LIST < 2 ? 'class="disabled"' : '',
                '>',
                '<a href="#" arial-label="Previous" onclick="PN_TBUSER_LIST=',
                PN_TBUSER_LIST < 2 ? 1 :PN_TBUSER_LIST-1,
                    ';return tbuser_list();">',
                        '<span class="glyphicon glyphicon-backward"',
                              'arial-hidden="true"></span>',
                    '</a>',
                '</li>',
                '<li class="disabled">',
                    '<a href="#">',
                        PN_TBUSER_LIST,
                        '<span class="sr-only">(current)</span>',
                    '</a>',
                '</li>',
                '<li ',
                PN_TBUSER_LIST == jsn["max_pn_tbusers"] ? 'class="disabled"' : '',
                '>',
                    '<a href="#" arial-label="Next" onclick="PN_TBUSER_LIST=',
                PN_TBUSER_LIST == jsn["max_pn_tbusers"] ? jsn["max_pn_tbusers"] : PN_TBUSER_LIST+1,
                        ';return tbuser_list();">',
                    '<span class="glyphicon glyphicon-forward"',
                              'arial-hidden="true"></span>',
                    '</a>',
                '</li>',
                '<li ',
                PN_TBUSER_LIST == jsn["max_pn_tbusers"] ? 'class="disabled"' : '',
                '>',
                    '<a href="#" arial-label="Last" onclick=PN_TBUSER_LIST="',
                    jsn["max_pn_tbusers"],
                        ';return tbuser_list();">',
                        '<span class="glyphicon glyphicon-step-forward"',
                              'arial-hidden="true"></span>',
                    '</a>',
                '</li>',
            '</ul>',
        '</nav>',
    '</div>'
    ].join('');
    $("#content").html(s);
    return false;
}

function tbuser_add_get() {
    var s=[
        '<p>用户名: <input id="bd_name" type="text" name="username" /></p>',
        '<p>密  码: <input id="bd_pw" type="password" name="password" /></p>',
        '<input type="button" name="" value="获取验证码" onclick="$(this).hide();$(\'#add_user2\').show();get_vcode();" />',
        '<div id="add_user2" style="display: none;">',
            '<p><img id="vcode_img" onclick="get_vcode();" />',
            '<input id="bd_vcodestr" type="hidden" name="vcodestr">',
            '<input id="verifycode" type="text"></p>',
            '<input type="button" id="btn_addtbuser" value="绑定" onclick="return tbuser_add_post();" disabled>',
        '</div>',
    ].join('');
    $("#content").html(s);
    return false;
}

function get_vcode() {
    $("#message").html("正在拉取验证码...");
    $(document).ready(function(){
        $.ajax({
            url:"/tbuser/getvercode",
            async:true,
            dataType:"json",
            type:'POST',
            data:{
                'tbuser_name': $("#bd_name").val()
            },
            complete: function(x,y) {
                $('#addbdid_submit').removeAttr('disabled');
            },
            success: function(x) {
                if (x["err_no"]=="0") {
                    $('#message').html("拉取成功,请输出图中的验证码,点击图片刷新验证码");
                    $("#vcode_img").attr("src","http://wappass.baidu.com/cgi-bin/genimage?"+x["vcodestr"]);
                    $("#bd_vcodestr").attr("value",x["vcodestr"]);
                    $('#btn_addtbuser').removeAttr('disabled');
                    
                } else {
                    $("#message").html(x["err_msg"]);
                }
            },
            error: function(x) {
                $("#message").html("操作失败，发生未知错误!");
            }
        });
    });
}

function tbuser_add_post() {
    var tbuser_name = $("#bd_name").val();
    $("#message").html("正在绑定...");
    $(document).ready(function(){
        $.ajax({
            url:"/tbuser/add",
            async:true,
            dataType:"json",
            type:'POST',
            data:{
                'tbuser_name': tbuser_name,
                'tbuser_pw': $("#bd_pw").val(),
                'verifycode': $("#verifycode").val(),
                'vcodestr': $("#bd_vcodestr").val(),
            },
            success: function(x) {
                if (x["err_no"] == "0") {
                    var s = [
                        '绑定成功。',
                        '<a href="#" onclick="return tbuser_add_get()">继续绑定贴吧用户</a>/',
                        '<a href="#" onclick="return tbuser_list()">查看贴吧用户列表</a>'
                    ].join("");
                    $("#message").html(s);
                    $("#content").html("");
                } else {
                    $("#message").html(x["err_msg"]);
                }
            },
            error: function(x) {
                $("#message").html("操作失败，发生未知错误!");
            }
        });
    });
    return false;
}

function tbuser_del(obj) {
    $("#message").html("正在解绑...");
    $(document).ready(function(){
        $.ajax({
            url:"/tbuser/del",
            async:true,
            dataType:"json",
            type:'POST',
            data:{
                'tbuid': $(obj).attr("tbuid")
            },
            success: function(x) {
                if (x["err_no"] == "0") {
                    $("#message").html("解绑成功");
                    $(obj).parent().parent().remove();
                    return false;
                } else {
                    $("#message").html(x["err_msg"]);
                    return false;
                }
            },
            error: function(x) {
                $("#message").html("操作失败，发生未知错误!");
                return false;
            }
        });
    });
    return false;
}

function has_set_tbuid() {
    if (CURRENT_TBUID == null) {
        $("#message").html("请先设置当前贴吧用户！");
        $("#content").html("");
        return false;
    }
    return true;
}
function tbuser_init() {
    var subutils = ''
        + '<ul class="nav nav-pills">'
            + '<li role="presentation" class="active">'
                + '<a href="#" id="tbuserlist" onclick="ch_subutil(this);return tbuser_list();">贴吧用户列表</a>'
            + '</li>'
            + '<li role="presentation">'
                + '<a href="#" id="add_tbuser" onclick="ch_subutil(this);return tbuser_add_get();">绑定贴吧帐号</a>'
            + '</li>'
        + '</ul>';
    $("#subutils").html(subutils);
    tbuser_list();
}
