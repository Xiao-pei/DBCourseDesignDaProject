$(document).ready(function (){
    $(".inputo").click(function(){
        $(this).css("background", "");
        $(this).css("border", "");
        $(".yesButton.register").attr("disabled", false)
        $(".yesButton.register").val("REGISTER")
        $(".yesButton.register").css("font-size", "18px")
    })
})

function inputBoxErrorStatus(boxId){
    $("#" + boxId).css("background", "#ff000014");
    $("#" + boxId).css("border", "1px solid rgb(255, 0, 0)");
}

function disableButton(info){
    $(".yesButton.register").attr("disabled", true)
    $(".yesButton.register").css("font-size", "15px")
    $(".yesButton.register").val(info)
}