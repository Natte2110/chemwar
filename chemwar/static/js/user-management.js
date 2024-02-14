$(document).ready(function () {
    $('#dataTable').DataTable();
});
document.getElementById("add-user").addEventListener("click", () => {
    $("#add-user-modal").modal("toggle")
})

const accountDeleteButtons = document.querySelectorAll(".delete-button");

accountDeleteButtons.forEach(function (element) {
    element.addEventListener("click", function () {
        let user_id = element.id.split("-")[1];
        console.log(user_id);
        let username = element.parentElement.parentElement.childNodes[3].innerHTML;
        $('#user-delete-check-div').html(`Are you sure you want to remove <b>${username}</b>?`)
        $("#delete-account-modal").modal("toggle")
        console.log(username)
        $("#delete-confirm").click(() => {
            console.log("deleted")
            fetch(`/delete-account`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: user_id
                }),
            })
            .then(response => response.json())
            .then(result => {
                console.log(result.success)
                if (result.success == true) {
                    location.reload()
                } else {
                    alert(result.message)
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        })
    });
});

$(document).ready(function () {

    const passwordVisibility = () => {
        if ($("#password").attr("type") === "password") {
            $("#password").attr("type", "text");
            $("#show-password").addClass("d-none");
            $("#hide-password").removeClass("d-none");
        } else {
            $("#password").attr("type", "password");
            $("#hide-password").addClass("d-none");
            $("#show-password").removeClass("d-none");
        }
    }

    $("#show-password").click(function () {
        passwordVisibility();
    });
    $("#hide-password").click(function () {
        passwordVisibility();
    });

    const confirmPasswordVisibility = () => {
        if ($("#confirm-password").attr("type") === "password") {
            $("#confirm-password").attr("type", "text");
            $("#show-confirm-password").addClass("d-none");
            $("#hide-confirm-password").removeClass("d-none");
        } else {
            $("#confirm-password").attr("type", "password");
            $("#hide-confirm-password").addClass("d-none");
            $("#show-confirm-password").removeClass("d-none");
        }
    }
    
    $("#show-confirm-password").click(function () {
        confirmPasswordVisibility();
    });
    $("#hide-confirm-password").click(function () {
        confirmPasswordVisibility();
    });

    $("#add-user-form").submit(function(event) {
        event.preventDefault();
        
        let password = $("input[name='password']").val();
        let confirmPassword = $("input[name='confirm-password']").val();
        let med_tag = ($("input[name='med-tag']").val() === "true") ? true : false;

        if (password!=confirmPassword) {
            alert("Passwords Must Match")
        } else {
            fetch(`/accounts`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: $("input[name='username']").val(),
                    password: password,
                    level:$("#level").val(),
                    group:$("#group").val(),
                    initial:$("input[name='initial']").val(),
                    surname:$("input[name='surname']").val(),
                    blood_group:$("#blood-type").val(),
                    med_tag:med_tag
                }),
            })
            .then(response => response.json())
            .then(result => {
                console.log(result.success)
                if (result.success == true) {
                    location.reload()
                } else {
                    alert(result.message)
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
      });
});

