$(document).ready(function () {

    $(".dateSelecterCell ").unbind("click").click(function(){
        $(this).addClass("selected")
        $(this).find(".dateLabel").addClass("light")
        $(this).find(".dateRadio").prop('checked', true);
        $(this).siblings().removeClass("selected").find(".dateLabel").removeClass("light")
    })

    $(".courseSelecterCell").hover(function () {
        if ($(this).hasClass("selected") || $(this).hasClass("disabled")) return
        $(this).addClass("avaliable")
        $(this).find(".courseAnimateDiv").stop().animate({ width: "4px" }, 300, 'easeOutExpo')
    }, function () {
        if ($(this).hasClass("selected") || $(this).hasClass("disabled")) return
        $(this).find(".courseAnimateDiv").stop().animate({ width: "0px" }, 200, 'easeInQuad')
    })

    $(".courseSelecterCell ").unbind("click").click(function () {
        if ($(this).hasClass("disabled")) {
            return
        }
        else if ($(this).hasClass("selected")) {
            $(this).removeClass("selected")
            $(this).find(".courseAnimateDiv").stop().animate({ width: "4px" }, 160, 'easeOutExpo')
            $(this).find(".courseIndex").removeClass("light")
            $(this).find(".classTimeLabel").removeClass("light")
            if ($(this).find(".courseCheckbox").prop('checked')) {
                $(this).find(".courseCheckbox").prop('checked', false);
            }
            return
        }
        else {
            $(this).addClass("selected")
            $(this).find(".courseAnimateDiv").stop().animate({ width: "500px" }, 300, 'easeOutExpo')
            $(this).find(".courseIndex").addClass("light")
            $(this).find(".classTimeLabel").addClass("light")
            if ($(this).find(".courseCheckbox").prop('checked') == false) {
                $(this).find(".courseCheckbox").prop('checked', true)
            }
        }
    })
})