function toggle_icon(span_id,juggment) {
    if (juggment) {
        $(span_id).attr("class","glyphicon glyphicon-ok form-control-feedback");
    } else {
        $(span_id).attr("class","glyphicon glyphicon-remove form-control-feedback");
    }
    validate_submit();
}

function juggment_user(content) {
    //长度 4-8
    if ((content.length<4) || (content.length>8)) {
        return false;
    }
    //没有空白符
    if (content.search(/\s/)!=-1) {
        return false;
    }
    username_ok=true;
    return true;
}

function juggment_password(content) {
    //长度 6-18
    if ((content.length<6) || (content.length>16)) {
        return false;
    }
    //字母和数字组合
    var has_char=false;
    var has_digit=false;
    for (var i=0; i < content.length; ++i) {
        if (content[i].match(/\d/)) {
            has_digit=true;
        } else if (content[i].match(/[a-zA-Z]/)){
            has_char=true;
        } else {
            return false;
        }
    }
    if (has_char && has_digit) {
        password_ok=true;
        return true;
    }
}

var username_ok=false;
var password_ok=false;
