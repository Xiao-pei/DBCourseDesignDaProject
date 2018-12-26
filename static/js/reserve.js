$(document).ready(function (){
    $(".reasonTextArea").bind('input propertychange',function (){
        console.log("a")
        if ($(this).val().length < 5){
            $(".submitButton").attr("disabled", true)
        } else {
            $(".submitButton").attr("disabled", false)
        }
    })
})