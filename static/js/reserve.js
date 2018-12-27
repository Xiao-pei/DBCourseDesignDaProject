$(document).ready(function (){
    $(".reasonTextArea").bind('input propertychange',function (){
        console.log("a")
        if ($(this).val().length < 5){
            $(".submitButton").attr("disabled", true)
        } else {
            $(".submitButton").attr("disabled", false)
        }
    })

    $(".reasonTextArea").focus(function (){
        $(".textareaContainer").addClass("focus")
    })

    $(".reasonTextArea").focusout(function (){
        $(".textareaContainer").removeClass("focus")
    })

    $(".reselectButton").click(function (event){
        window.open("/search/time", "_self");
    })
})