var PN_TBLIST = 1;
var PN_SIGNRECORDS = 1;

function get_tblist() {
    if (!has_set_tbuid()) { return false; }
    $("#message").html("正在获取贴吧列表...");
    $("#content").html("");
    $(document).ready(function(){
        $.ajax({
            url:"/tblist/get",
            async:true,
            dataType:"json",
            type:'POST',
            data:{
                'pn': PN_TBLIST,
                'tbuid': CURRENT_TBUID,
            },
            complete: function(x,y) {
                ;
            },
            success: function(x) {
                $("#message").html("");
                return parse_tblist(x);
            },
            error: function(x) {
                $("#message").html("操作失败，发生未知错误!");
            }
        });
    });
    return false;
}

function parse_tblist(jsn) {
    var s = '';
    if (jsn["count_tblist"] == 0) {
        s += [
            "你还没有关注的吧，或还未",
            '<a href="#" onclick="return update_tblist();">更新贴吧列表</a>'
        ].join('');
        $("#content").html(s);
        return false;
    }
    s += [
        "如实际情况发生变化，可立即",
        '<a href="#" onclick="return update_tblist();">更新贴吧列表</a>'
    ].join('');
    s += [
        '<div class="panel panel-primary">',
            '<div class="panel-heading">',
                '共绑定'+jsn["count_tblist"]+'个贴吧用户。',
            '</div>',
            '<table class="table">',
                '<thead>',
                    '<tr>',
                        '<th>#</th>',
                        '<th>贴吧名</th>',
                        '<th>贴吧ID</th>',
                        '<th>今日是否签到</th>',
                    '</tr>',
                '</thead>',
                '<tbody>',
    ].join('');
    for (var i=0; i < jsn["tblist"].length; ++i) {
        s += [
            '<tr>',
                '<th scope="row">' ,  (jsn["pn_tblist"]-1)*jsn["num_per_tbusers"]+i+1 , '</th>',
                '<td>', jsn["tblist"][i]["tb_name"] , '</td>',
                '<td>', jsn["tblist"][i]["tb_id"] , '</td>',
                '<td>', jsn["tblist"][i]["signed"]==1 ? "是": "否", '</td>',
            '</tr>',
        ].join('');
    }
    s += [
                '</tbody>',
            '</table>',
            gen_pagernav(PN_TBLIST, jsn["max_pn_tblist"], "PN_TBLIST", "return get_tblist()"),
        '</div>'
    ].join('');
    $("#content").html(s);
    return false;
}

function update_tblist() {
    if (!has_set_tbuid()) { return false; }
    $("#message").html("正在提交请求...");
    $("#content").html("");
    $(document).ready(function(){
        $.ajax({
            url:"/tblist/update",
            async:true,
            dataType:"json",
            type:'POST',
            data:{
                'tbuid': CURRENT_TBUID,
            },
            complete: function(x,y) {
                ;
            },
            success: function(x) {
                $("#message").html(x["err_msg"]);
            },
            error: function(x) {
                $("#message").html("操作失败，发生未知错误!");
            }
        });
    });
    return false;
    
}

function get_signrecords() {
    if (!has_set_tbuid()) { return false; }
    $("#message").html("正在获取签到记录...");
    $("#content").html("");
    $(document).ready(function(){
        $.ajax({
            url:"/sign/get",
            async:true,
            dataType:"json",
            type:'POST',
            data:{
                'pn': PN_SIGNRECORDS,
                'tbuid': CURRENT_TBUID,
            },
            complete: function(x,y) {
                ;
            },
            success: function(x) {
                $("#message").html("");
                return parse_signrecords(x);
            },
            error: function(x) {
                $("#message").html("操作失败，发生未知错误!");
            }
        });
    });
    return false;
    
}

function parse_signrecords(jsn) {
    var s = '';
    if (jsn["count_signrecords"] == 0) {
        s += [
            "你还没有签到记录，你可以考虑",
            '<a href="#" onclick="return sign_now();">立即签到</a>'
        ].join('');
        $("#content").html(s);
        return false;
    }
    s += [
        "如实际情况发生变化，可立即",
        '<a href="#" onclick="return update_tblist();">更新贴吧列表</a>'
    ].join('');
    s += [
        '<div class="panel panel-primary">',
            '<div class="panel-heading">',
                '共'+jsn["count_signrecords"]+'个签到记录。',
            '</div>',
            '<table class="table">',
                '<thead>',
                    '<tr>',
                        '<th>#</th>',
                        '<th>贴吧名</th>',
                        '<th>签到日期</th>',
                        '<th>签到签到返回码</th>',
                    '</tr>',
                '</thead>',
                '<tbody>',
    ].join('');
    for (var i=0; i < jsn["signrecords"].length; ++i) {
        s += [
            '<tr>',
                '<th scope="row">' ,  (jsn["pn_signrecords"]-1)*jsn["num_per_signrecords"]+i+1 , '</th>',
                '<td>', jsn["signrecords"][i]["tb_name"] , '</td>',
                '<td>', jsn["signrecords"][i]["sign_date"] , '</td>',
                '<td>', jsn["signrecords"][i]["err_no"], '</td>',
            '</tr>',
        ].join('');
    }
    s += [
                '</tbody>',
            '</table>',
            gen_pagernav(PN_SIGNRECORDS, jsn["max_pn_signrecords"], "PN_SIGNRECORDS", "return get_signrecords()"),
        '</div>'
    ].join('');
    $("#content").html(s);
    return false;
}

function sign_now() {
    if (!has_set_tbuid()) { return false; }
    $("#message").html("正在提交请求...");
    $("#content").html("");
    $(document).ready(function(){
        $.ajax({
            url:"/sign/signnow",
            async:true,
            dataType:"json",
            type:'POST',
            data:{
                'tbuid': CURRENT_TBUID,
            },
            complete: function(x,y) {
                ;
            },
            success: function(x) {
                if (x["err_no"]=='17') {
                    $("#message").html(x["err_msg"]);
                }
                if (x["err_no"]=='15') {
                    var s = '，预计'+x["sign_times"]+"分钟后完成。";
                    $("#message").html(x["err_msg"]+s);
                }
            },
            error: function(x) {
                $("#message").html("操作失败，发生未知错误!");
            }
        });
    });
    return false;
}

function sign_init() {
    var subutils = ''
        + '<ul class="nav nav-pills">'
            + '<li role="presentation" class="active">'
                + '<a href="#" id="tblist" onclick="ch_subutil(this);return get_tblist();">贴吧列表</a>'
            + '</li>'
            + '<li role="presentation">'
                + '<a href="#" id="signrecords" onclick="ch_subutil(this);return get_signrecords();">签到记录</a>'
            + '</li>'
        + '</ul>';
    $("#subutils").html(subutils);
    get_tblist();
}
