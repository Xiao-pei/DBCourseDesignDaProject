$(document).ready(function () {

    $(".classRoomButton").hover(function (){
        $(this).removeClass("wide")
        $(this).find(".nextIndicator").removeClass("hidden")
    },
    function (){
        $(this).addClass("wide")
        $(this).find(".nextIndicator").addClass("hidden")
    })

    $(".classRoomButton").unbind("click").click(function (){
        window.open($(this).data("href"), "_self");
    })
})