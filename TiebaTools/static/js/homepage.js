var LOADED_UTILS = [];

/* Nano Templates - https://github.com/trix/nano */
function nano(template, data) {
  return template.replace(/\{([\w\.]*)\}/g, function(str, key) {
    var keys = key.split("."), v = data[keys.shift()];
    for (var i = 0, l = keys.length; i < l; i++) v = v[keys[i]];
    return (typeof v !== "undefined" && v !== null) ? v : "";
  });
}

function ch_active(obj) {
    $(obj).siblings().removeClass("active")
        .end().addClass("active");
}

function ch_subutil(obj) {
    $(obj).parent().siblings().removeClass("active")
        .end().addClass("active");
}

function ch_tab(obj) {
    var o1=$(obj).parent();
    o1.siblings().attr("class","");
    o1.attr("class","active");
    var o2=$(document.getElementById($(obj).attr("tid")));
    o2.siblings().attr("class","tab-pane");
    o2.attr("class","tab-pane active");
}

function load_utils(util) {
    if ($.inArray(util, LOADED_UTILS)==-1) {
        $.getScript('/static/js/'+util+'.js', function () {
            LOADED_UTILS.push(util);
            window[util+"_init"]();
        });
    } else {
        window[util+"_init"]();
        return false;
    }
}

function gen_pagernav(pn,max_pn, pn_str, onclick_str) {
    var data = {
        "pn_1_able": (pn < 2 ? 'class="disabled"' : ''),
        "pn_pre_able": (pn < 2 ? 'class="disabled"' : ''),
        "pn_pre": (pn < 2 ? 1 : pn-1),
        "pn": pn,
        "pn_next_able": (pn==max_pn ? 'class="disabled"' : ''),
        "pn_next": (pn == max_pn ? max_pn : pn+1),
        "pn_max_able": (pn==max_pn ? 'class="disabled"' : ''),
        "max_pn": max_pn,
        "pn_str": pn_str,
        "onclick_str": onclick_str,
    };
    var s = [
        '<nav>',
            '<ul class="pager">',
                '<li {pn_1_able}>',
                    '<a href="#" arial-label="First" onclick="{pn_str}=1;{onclick_str};">',
                        '<span class="glyphicon glyphicon-step-backward" arial-hidden="true"></span>',
                    '</a>',
                '</li>',
                '<li {pn_pre_able}>',
                    '<a href="#" arial-label="Previous" onclick="{pn_str}={pn_pre};{onclick_str};">',
                        '<span class="glyphicon glyphicon-backward" arial-hidden="true"></span>',
                    '</a>',
                '</li>',
                '<li class="disabled">',
                    '<a href="#">{pn}',
                        '<span class="sr-only">(current)</span>',
                    '</a>',
                '</li>',
                '<li {pn_next_able}>',
                    '<a href="#" arial-label="Next" onclick="{pn_str}={pn_next};{onclick_str};">',
                        '<span class="glyphicon glyphicon-forward" arial-hidden="true"></span>',
                    '</a>',
                '</li>',
                '<li {pn_max_able}>',
                    '<a href="#" arial-label="Next" onclick="{pn_str}={max_pn};{onclick_str};">',
                        '<span class="glyphicon glyphicon-step-forward" arial-hidden="true"></span>',
                    '</a>',
                '</li>',
            '</ul>',
        '</nav>',
    ].join('');
    return nano(s,data);
}

load_utils("tbuser");
