$(document).ready(function (){
    $(".inputo").click(function(){
        $(this).css("background", "");
        $(this).css("border", "");
        $(".yesButton.login").attr("disabled", false)
        $(".yesButton.login").val("SIGN IN")
        $(".yesButton.login").css("font-size", "18px")
    })
})

function inputBoxErrorStatus(boxId){
    $("#" + boxId).css("background", "#ff000014");
    $("#" + boxId).css("border", "1px solid rgb(255, 0, 0)");
}

function disableButton(){
    $(".yesButton.login").attr("disabled", true)
    $(".yesButton.login").css("font-size", "15px")
    $(".yesButton.login").val("INCORRECT PASSWORD OR USERNAME")
}