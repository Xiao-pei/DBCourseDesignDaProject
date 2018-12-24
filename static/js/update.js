
$(document).ready(function (){
    $("#updateButton").click(function (){
        showChangeAlert()
    })
})

function setPasswordInputChangeEvent(){
    $("#passwordInput").change(function (){
        $("#password").val($(this).val())
    })
}

function showChangeAlert() {

    var alertContent = ''

        alertContent += "Username: " + $("#username").val() + "\n\n"

  
        alertContent += "Real Name: " + $("#real_name").val() + "\n\n"
    
        alertContent += "Telephone Number: " + $("#tel").val() + "\n\n"

    alertContent += "Enter password to apply.\n"

        swal({
            closeOnClickOutside: false,
            title: "Here's your new profile",
            text: alertContent,
            content: {

                element: "input",
                attributes: {
                    className: "inputo",
                    type: "password",
                    id: "passwordInput",
                },

            },
            buttons: {
                cancel: true,
                button: {
                    text: "Confirm",
                    className: "input submitButton",
                },
            },
        });
        setPasswordInputChangeEvent()
        $(".submitButton").click(function () {
            $("#submit").click()
        })
}

function wrongPassword(){
    swal({
        closeOnClickOutside: false,
        title: "WRONG PASSWORD!",
        //icon: "error",
        text: "Please enter password again",
        content: {
            element: "input",
            attributes: {
                className: "inputo",
                type: "password",
            },
        },
        buttons: {
            cancel: true,
            confirm: {
                text: "Confirm",
                className: "input submitButton",
            },
        },
    });
    $(".submitButton").click(function () {
        $("#submit").click()
    })
}