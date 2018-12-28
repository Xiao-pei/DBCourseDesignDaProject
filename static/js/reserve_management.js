$(document).ready(function (){
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

    $(".approveButton").unbind("click").click(function (){
        $(".approve").click()
    })
    
    $(".refuseButton").unbind("click").click(function (){
        $(".disapprove").click()
    })

})
