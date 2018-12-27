$(document).ready(function (){
    $(".topBarButton, .messageButton, .messageButton, allReservationButton, .innerTitleButton ").click( function(event){
        console.log(":fdsff")
        if ($(this).data("href") != ""){
            window.open($(this).data("href"), "_self");
        }
    })
})
