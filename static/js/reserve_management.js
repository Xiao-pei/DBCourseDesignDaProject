$(document).ready(function (){
    $(".approveButton").click(function (){
        $(".approve").click()
    })
    
    $(".refuseButton").click(function (){
        $(".disapprove").click()
    })

    $(".sectionTitleButton").unbind("click").click(function (){
        if ($(this).data("href") != ""){
            window.open($(this).data("href"), "_blank");
        }
    })

    $(".topBarButton").unbind("click").click(function (){
        if ($(this).data("href") != ""){
            window.open($(this).data("href"), "_self");
        }
    })

})
