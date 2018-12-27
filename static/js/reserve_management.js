$(document).ready(function (){
    $(".approveButton").click(function (event){
        $(".approve").click()
    })
    
    $(".refuseButton").click(function (event){
        $(".disapprove").click()
    })

    $(".sectionTitleButton").unbind("click").click(function (event){
        if ($(this).data("href") != ""){
            window.open($(this).data("href"), "_blank");
        }
    })

    $(".topBarButton").unbind("click").click(function (event){
        if ($(this).data("href") != ""){
            window.open($(this).data("href"), "_self");
        }
    })

})
