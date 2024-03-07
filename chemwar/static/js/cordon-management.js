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
            fetch(`/delete-cordon`, {
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

    $("#add-user-form").submit(function(event) {
        event.preventDefault();
        
        let down_wind = ($("input[name='down_wind']").val() === "true") ? true : false;

        fetch(`/cordon-management`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cordon_name: $("input[name='cordon_name']").val(),
                cordon_size:$("input[name='cordon_size']").val(),
                down_wind:down_wind,
                down_wind_size:$("input[name='down_wind_size']").val(),
                cbrn_type:$("#cbrn_type").val(),
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
        
      });
});

