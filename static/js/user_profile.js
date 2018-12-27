$(document).ready(function (){
    $(".innerTitleButton").click(function (){
        if ($(this).data("herf") != ""){
            window.open($(this).data("herf"), "_self");
        }
    })
    
    $(".messageButton").click(function (){
        if ($(this).data("herf") != ""){
            window.open($(this).data("herf"), "_self");
        }
    })

    $(".allReservationButton").click(function (){
        if ($(this).data("herf") != ""){
            window.open($(this).data("herf"), "_self");
        }
    })
})
