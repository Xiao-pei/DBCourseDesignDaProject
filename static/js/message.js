$(document).ready(function (){

    $(".messageListCellTitleContainer").hover(function (event){
        $(this).find(".userName").addClass("hover")
    },
    function (event){
        $(".userName").removeClass("hover")
    })

    $("div, span").click(function (event){
        if ($(this).data("href") != ""){
            window.open($(this).data("href"), "_self");
        }
    })
})