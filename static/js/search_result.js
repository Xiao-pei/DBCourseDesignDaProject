$(document).ready(function () {
    let classroom = "{{ url_for('reserve',room_id=room['id'],begin=begin,end=end,date=date)}}"

    $(".classRoomButton").hover(function (){
        $(this).removeClass("wide")
        $(this).find(".nextIndicator").removeClass("hidden")
    },
    function (){
        $(this).addClass("wide")
        $(this).find(".nextIndicator").addClass("hidden")
    })

    $(".classRoomButton").unbind("click").click(function (){
        window.open($(this).data("herf"), "_self");
    })
})