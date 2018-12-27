$(document).ready(function (){

    $(".blah").hover(function (event){
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

    $(".messageTextArea").bind('input propertychange',function (){
        console.log("a")
        if ($(this).val().length < 5){
            $(".submitButton").attr("disabled", true)
        } else {
            $(".submitButton").attr("disabled", false)
        }
    })
})