var selectedClassNum = 0
$(document).ready(function () {

    $(".dateSelecterCell ").unbind("click").click(function (event){
        $(this).addClass("selected")
        $(this).find(".dateLabel").addClass("light")
        $(this).find(".dateRadio").prop('checked', true);
        $(this).siblings().removeClass("selected").find(".dateLabel").removeClass("light")
    })

    $(".courseSelecterCell").hover(function () {
        if ($(this).hasClass("selected") || $(this).hasClass("disabled")) return
        $(this).find(".courseAnimateDiv").stop().animate({ width: "4px" }, 300, 'easeOutExpo')
    }, function () {
        if ($(this).hasClass("selected") || $(this).hasClass("disabled")) return
        $(this).find(".courseAnimateDiv").stop().animate({ width: "0px" }, 200, 'easeInQuad')
    })

    $(".courseSelecterCell ").unbind("click").click(function (event){
        if ($(this).hasClass("disabled")) {
            return
        }
        else if ($(this).hasClass("selected")) {
            $(this).removeClass("selected")
            $(this).find(".courseAnimateDiv").stop().animate({ width: "4px" }, 160, 'easeOutExpo')
            $(this).find(".courseIndex").removeClass("light")
            $(this).find(".classTimeLabel").removeClass("light")
            selectedClassNum -= 1
            refreshClassButtons()
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
            selectedClassNum += 1
            refreshClassButtons()
            if ($(this).find(".courseCheckbox").prop('checked') == false) {
                $(this).find(".courseCheckbox").prop('checked', true)
            }
        }
    })

    $(".campusSelecterCell ").unbind("click").click(function (event){
        $(this).addClass("selected")
        $(this).siblings().removeClass("selected").find(".campusLabel").removeClass("light")
        $(this).siblings().find(".locationButton").removeClass("light")
        $(this).siblings().find(".locationIcon").removeClass("light")
        $(this).find(".campusLabel").addClass("light")
        $(this).find(".locationButton").addClass("light")
        $(this).find(".locationIcon").addClass("light")
        $(this).find(".campusRadio").prop('checked', true);
    })

    $(".locationButton").unbind("click").click(function (e) {
        e.stopPropagation();
        var hrefURL = "https://www.google.com/maps/"
        if ($(this).attr('id') == "locate0") {
            hrefURL += "@30.6301606,104.0844545,16z"
        } else if ($(this).attr('id') == "locate1") {
            hrefURL += "@30.6399605,104.0712453,17z"
        } else {
            hrefURL += "@30.5580034,103.9997657,16z"
        }
        window.open(hrefURL, "_blank");
    })
})

function refreshClassButtons() {
    if (selectedClassNum == 0) {
        $(".courseSelecterCell ").removeClass("disabled")
        return
    }
    $(".courseSelecterCell").addClass("disabled")
    $(".courseSelecterCell.selected").last().removeClass("disabled").nextAll(".courseSelecterCell.disabled").eq(0).removeClass("disabled")
    $(".courseSelecterCell.selected").first().removeClass("disabled").prevAll(".courseSelecterCell.disabled").eq(0).removeClass("disabled")
}