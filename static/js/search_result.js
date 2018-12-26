$(document).ready(function () {
    let classroom = "{{ url_for('reserve',room_id=room['id'],begin=begin,end=end,date=date) }}"

    $(".classRoomButton").unbind("hover").hover(function (){
        $(this).animate({ paddingLeft: "0px", paddingRight: "0px"  }, 300)
        $(this).find(".nextIndicator").animate({ width: "24px" }, 300)
    },
    function (){
        $(this).animate({ paddingLeft: "2px", paddingRight: "22px"  }, 300)
        $(this).find(".nextIndicator").animate({ width: "0px" }, 300)
    })
})