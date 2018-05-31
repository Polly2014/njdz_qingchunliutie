// JavaScript Document
$(".table table tr").eq(0).find("th").addClass("curr");
$(".table table tr").eq(1).find("td").addClass("curr");
$(".table table tr").eq(2).find("td").addClass("curr");


var maxtime = 60 * 3 //一个小时，按秒计算，自己调整!
function CountDown() {
    if (maxtime >= 0) {
        minutes = Math.floor(maxtime / 60);
        seconds = Math.floor(maxtime % 60);
        msg = "剩余时间" + minutes + "分" + seconds + "秒";
        document.all["timer"].innerHTML = msg;
        if (maxtime == 1 * 60) alert('注意，还有1分钟!');
        --maxtime; /// <reference path="../bin/" />

    }
    else {
        clearInterval(timer);
        var score = $("#span3").html();
        var Lb = $("#HiddenField1").val();
        var temp_ip = $("#HiddenField3").val();
        if (Lb == "主题竞赛") {
            window.location.href = "InfoZhuTi.aspx?score=" + score + "&Lb=" + Lb + "&temp_ip=" + temp_ip + "&time=0"; //maxtime=0
        }
        else {
            window.location.href = "InfoZhuanYe.aspx?score=" + score + "&Lb=" + Lb + "&temp_ip=" + temp_ip + "&time=0";
        }
        alert("时间到，结束!");
    }
}
timer = setInterval("CountDown()", 1000);
function GetQuestion() {
    var score = $("#span3").html();
    var step = $("#Span2").html();
    var Lb = $("#HiddenField1").val();
    var count = $("#HiddenField2").val();
    var answer = "";
    var Ans = document.getElementsByName("choose");
    for (i = 0; i < Ans.length; i++) {
        if (Ans[i].checked) {
            answer = Ans[i].value;
        }
    }
    if (answer != "") {
        answer += "|"
    }
    else {
        $('input[name="ck"]:checked').each(function () {
            answer += $(this).val() + "|";
        });
    }

    $.ajax({
        type: "POST",
        //        url: "GetQuestion.ashx",
        url: "DataYY.aspx",
        data: {
            step: step,
            answer: answer,
            score: score,
            count: count
        },
        success: function (data) {
            var obj = eval("(" + data + ")");
            if (obj.success == "false") {
                window.location.href = "InfoZhuTi.aspx?score=" + obj.SCORE + "&Lb=" + Lb + "&time=" + (maxtime + 1) + "&count=" + count;
            }
            else {
                $("#Span1").html(obj.data);
                $("#Span2").html(obj.Stage);
                $("#span3").html(obj.SCORE);
            }
        }
    });
}
function GetQuestion1() {
    var score = $("#span3").html();
    var step = $("#Span2").html();
    var Lb = $("#HiddenField1").val();
    var count = $("#HiddenField2").val();
    var answer = "";
    $.ajax({
        type: "POST",
        //        url: "GetQuestion.ashx",
        url: "DataYY.aspx",
        data: {
            step: step,
            answer: answer,
            score: score,
            count: count
        },
        success: function (data) {
            var obj = eval("(" + data + ")");
            if (obj.success == "false") {
                clearInterval(timer);
                window.location.href = "InfoZhuTi.aspx?score=" + obj.SCORE + "&Lb=" + Lb + "&time=" + (maxtime + 1) + "&count=" + count;
            }
            else {
                $("#Span1").html(obj.data);
                $("#Span2").html(obj.Stage);
                $("#span3").html(obj.SCORE);
            }
        }
    });
}
function GetScore() {
    var Department = $("#Department").val();
    var Name = $("#Name").val();
    var Phone = $("#Phone").val();
    var Weixin = $("#Weixin").val();
    var score = $("#HiddenField1").val();
    var lb = $("#HiddenField2").val();
    var time = $("#HiddenField3").val();
    var tempid = $("#HiddenField4").val();
    if (Department == "") {
        alert("车间部门不能为空！");
        return;
    }
    if (Name == "") {
        alert("姓名不能为空！");
        return;
    }
    if (Phone == "" && Weixin == "") {
        alert("手机号、微信号需至少填写一项！");
        return;
    }
    if (Phone != "") {
        var reg = /^1[3|4|5|8][0-9]\d{4,8}$/;
        var c = reg.test(Phone);
        if (c == false) {
            alert("请输入正确的手机号码！");
            return;
        }
    }
    //window.location.href = "Score.aspx?Department=" + Department + "&Name=" + Name + "&Phone=" + Phone + "&Weixin=" + Weixin + "&lb=" + lb + "&score=" + score + "&time=" + time + "&id=" + tempid;
    window.location.href = "/score/";
}
function GetQuestionTY() {
    var score = $("#span3").html();
    var step = $("#Span2").html();
    var Lb = $("#HiddenField1").val();
    var count = $("#HiddenField2").val();
    var answer = "";
    var Ans = document.getElementsByName("choose");
    for (i = 0; i < Ans.length; i++) {
        if (Ans[i].checked) {
            answer = Ans[i].value;
        }
    }
    if (answer != "") {
        answer += "|"
    }
    else {
        $('input[name="ck"]:checked').each(function () {
            answer += $(this).val() + "|";
        });
    }
    $.ajax({
        type: "POST",
        //        url: "GetQuestionTY.ashx",
        url: "DataYY.aspx",
        data: {
            step: step,
            answer: answer,
            score: score,
            count: count
        },
        success: function (data) {
            var obj = eval("(" + data + ")");
            if (obj.success == "false") {
                window.location.href = "InfoZhuanYe.aspx?score=" + obj.SCORE + "&Lb=" + Lb + "&time=" + (maxtime + 1) + "&count=" + count;
            }
            else {
                $("#Span1").html(obj.data);
                $("#Span2").html(obj.Stage);
                $("#span3").html(obj.SCORE);
            }
        }
    });
}
function GetQuestionTY1() {
    var score = $("#span3").html();
    var step = $("#Span2").html();
    var Lb = $("#HiddenField1").val();
    var count = $("#HiddenField2").val();
    var answer = "";
    $.ajax({
        type: "POST",
        //        url: "GetQuestionTY.ashx",
        url: "DataYY.aspx",
        data: {
            step: step,
            answer: answer,
            score: score,
            count: count
        },
        success: function (data) {
            var obj = eval("(" + data + ")");
            if (obj.success == "false") {
                window.location.href = "InfoZhuanYe.aspx?score=" + obj.SCORE + "&Lb=" + Lb + "&time=" + (maxtime + 1) + "&count=" + count;
            }
            else {
                $("#Span1").html(obj.data);
                $("#Span2").html(obj.Stage);
                $("#span3").html(obj.SCORE);
            }
        }
    });
}

function GetQuestionYY() {
    var score = $("#span3").html();
    var step = $("#Span2").html();
    var Lb = $("#HiddenField1").val();
    var count = $("#HiddenField2").val();
    var answer = "";
    var Ans = document.getElementsByName("choose");
    for (i = 0; i < Ans.length; i++) {
        if (Ans[i].checked) {
            answer = Ans[i].value;
        }
    }
    if (answer != "") {
        answer += "|"
    }
    else {
        $('input[name="ck"]:checked').each(function () {
            answer += $(this).val() + "|";
        });
    }
    $.ajax({
        type: "POST",
        //        url: "GetQuestionYY.ashx",
        url: "DataYY.aspx",
        data: {
            step: step,
            answer: answer,
            score: score,
            count: count
        },
        success: function (data) {
            var obj = eval("(" + data + ")");
            if (obj.success == "false") {
                window.location.href = "InfoZhuanYe.aspx?score=" + obj.SCORE + "&Lb=" + Lb + "&time=" + (maxtime + 1) + "&count=" + count;
            }
            else {
                $("#Span1").html(obj.data);
                $("#Span2").html(obj.Stage);
                $("#span3").html(obj.SCORE);
            }
        }
    });
}
function GetQuestionYY1() {
    var score = $("#span3").html();
    var step = $("#Span2").html();
    var Lb = $("#HiddenField1").val();
    var count = $("#HiddenField2").val();
    var answer = "";
    $.ajax({
        type: "POST",
        //        url: "GetQuestionYY.ashx",
        url: "DataYY.aspx",
        data: {
            step: step,
            answer: answer,
            score: score,
            count: count
        },
        success: function (data) {
            var obj = eval("(" + data + ")");
            if (obj.success == "false") {
                window.location.href = "InfoZhuanYe.aspx?score=" + obj.SCORE + "&Lb=" + Lb + "&time=" + (maxtime + 1) + "&count=" + count;
            }
            else {
                $("#Span1").html(obj.data);
                $("#Span2").html(obj.Stage);
                $("#span3").html(obj.SCORE);
            }
        }
    });
}

function GetQuestionJX() {
    var score = $("#span3").html();
    var step = $("#Span2").html();
    var Lb = $("#HiddenField1").val();
    var count = $("#HiddenField2").val();
    var answer = "";
    var Ans = document.getElementsByName("choose");
    for (i = 0; i < Ans.length; i++) {
        if (Ans[i].checked) {
            answer = Ans[i].value;
        }
    }
    if (answer != "") {
        answer += "|"
    }
    else {
        $('input[name="ck"]:checked').each(function () {
            answer += $(this).val() + "|";
        });
    }
    $.ajax({
        type: "POST",
        //        url: "GetQuestionJX.ashx",
        url: "DataYY.aspx",
        data: {
            step: step,
            answer: answer,
            score: score,
            count: count
        },
        success: function (data) {
            var obj = eval("(" + data + ")");
            if (obj.success == "false") {
                window.location.href = "InfoZhuanYe.aspx?score=" + obj.SCORE + "&Lb=" + Lb + "&time=" + (maxtime + 1) + "&count=" + count;
            }
            else {
                $("#Span1").html(obj.data);
                $("#Span2").html(obj.Stage);
                $("#span3").html(obj.SCORE);
            }
        }
    });
}
function GetQuestionJX1() {
    var score = $("#span3").html();
    var step = $("#Span2").html();
    var Lb = $("#HiddenField1").val();
    var count = $("#HiddenField2").val();
    var answer = "";
    $.ajax({
        type: "POST",
        //        url: "GetQuestionJX.ashx",
        url: "DataYY.aspx",
        data: {
            step: step,
            answer: answer,
            score: score,
            count: count
        },
        success: function (data) {
            var obj = eval("(" + data + ")");
            if (obj.success == "false") {
                window.location.href = "InfoZhuanYe.aspx?score=" + obj.SCORE + "&Lb=" + Lb + "&time=" + (maxtime + 1) + "&count=" + count;
            }
            else {
                $("#Span1").html(obj.data);
                $("#Span2").html(obj.Stage);
                $("#span3").html(obj.SCORE);
            }
        }
    });
}

function GetQuestionDT() {
    var score = $("#span3").html();
    var step = $("#Span2").html();
    var Lb = $("#HiddenField1").val();
    var count = $("#HiddenField2").val();
    var answer = "";
    var Ans = document.getElementsByName("choose");
    for (i = 0; i < Ans.length; i++) {
        if (Ans[i].checked) {
            answer = Ans[i].value;
        }
    }
    if (answer != "") {
        answer += "|"
    }
    else {
        $('input[name="ck"]:checked').each(function () {
            answer += $(this).val() + "|";
        });
    }
    $.ajax({
        type: "POST",
        //        url: "GetQuestionDT.ashx",
        url: "DataYY.aspx",
        data: {
            step: step,
            answer: answer,
            score: score,
            count: count
        },
        success: function (data) {
            var obj = eval("(" + data + ")");
            if (obj.success == "false") {
                window.location.href = "InfoZhuanYe.aspx?score=" + obj.SCORE + "&Lb=" + Lb + "&time=" + (maxtime + 1) + "&count=" + count;
            }
            else {
                $("#Span1").html(obj.data);
                $("#Span2").html(obj.Stage);
                $("#span3").html(obj.SCORE);
            }
        }
    });
}
function GetQuestionDT1() {
    var score = $("#span3").html();
    var step = $("#Span2").html();
    var Lb = $("#HiddenField1").val();
    var count = $("#HiddenField2").val();
    var answer = "";
    $.ajax({
        type: "POST",
        //        url: "GetQuestionDT.ashx",
        url: "DataYY.aspx",
        data: {
            step: step,
            answer: answer,
            score: score,
            count: count
        },
        success: function (data) {
            var obj = eval("(" + data + ")");
            if (obj.success == "false") {
                window.location.href = "InfoZhuanYe.aspx?score=" + obj.SCORE + "&Lb=" + Lb + "&time=" + (maxtime + 1) + "&count=" + count;
            }
            else {
                $("#Span1").html(obj.data);
                $("#Span2").html(obj.Stage);
                $("#span3").html(obj.SCORE);
            }
        }
    });
}