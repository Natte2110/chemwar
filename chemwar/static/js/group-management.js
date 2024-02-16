$(document).ready(function () {
    $('#dataTable').DataTable();
});

document.getElementById("add-group").addEventListener("click", () => {
    $("#add-group-modal").modal("toggle")
})

$("#add-group-form").submit(function (event) {
    event.preventDefault();

    let groupName = $("input[name='group-name']").val();

    fetch(`/groups`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            group_name: groupName,
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

const groupDeleteButtons = document.querySelectorAll(".delete-button");

groupDeleteButtons.forEach(function (element) {
    element.addEventListener("click", function () {
        let group_id = element.id.split("-")[1];
        let groupName = element.parentElement.parentElement.childNodes[3].innerHTML;
        $('#group-delete-check-div').html(`Are you sure you want to remove <b>${groupName}</b>?`)
        $("#delete-group-modal").modal("toggle")
        $("#delete-confirm").click(() => {
            fetch(`/delete-group`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: group_id
                }),
            })
                .then(response => response.json())
                .then(result => {
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

const groupManageButtons = document.querySelectorAll(".group-manage");

const createUserTable = (result, groupName, groupID) => {
    let tableHTML = `
    <div class="card shadow mb-4">
        <div class="card-header py-3">
            <h5 id="${groupID}" class="m-0 font-weight-bold users-table-title">${groupName}</h5>
            <a href="#" id="add-user-group" class="d-none d-inline-block btn btn-sm btn-success shadow-sm">
                <i class="fas fa-plus fa-sm text-white-50" aria-hidden="true"></i> Add User</a>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Surname</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>`;

    result.users.forEach(user => {
        tableHTML += `
            <tr>
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.surname}</td>
                <td class="text-center text-danger">
                <a href="#" id="remove-${user.id}"class="d-none d-inline-block btn btn-sm btn-danger remove-user shadow-sm">
                        <i class="fas fa-minus fa-sm text-white-50" aria-hidden="true"></i>
                    </a>
                </td>
            </tr>`;
    });

    tableHTML += `</tbody>
                        </table>
                        </div>
                    </div>
                </div>`;

    $("#group-management-table").html(`${tableHTML}`);

    document.getElementById("add-user-group").addEventListener("click", () => {
        $("#add-user-to-group-modal").modal("toggle");
        $("#add-user-to-group-form").attr('class', '');
        $("#add-user-to-group-form").attr('class', groupID);
    })

    $(document).ready(function () {
        $('#group-table').DataTable();
    });

    const removeUserButtons = document.querySelectorAll(".remove-user");

    removeUserButtons.forEach(function (element) {
        element.addEventListener("click", function () {
            let userID = element.id.split("-")[1];
            let groupID = 2
            console.log(userID, groupName)
            fetch(`/add-user-group`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userID,
                    group_id: groupID
                })
            })
                .then(response => response.json())
                .then(result => {
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
}

groupManageButtons.forEach(function (element) {
    element.addEventListener("click", function () {
        let groupID = element.id.split("-")[1];
        let groupName = element.parentElement.parentElement.childNodes[3].innerHTML;

        fetch(`/group-users/${groupID}`)
            .then(response => response.json())
            .then(result => {
                createUserTable(result, groupName, groupID)

            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });
});

$("#add-user-to-group-form").submit(function (event) {
    event.preventDefault();

    let userID = $("select[name='user-list']").val();
    let groupID = $("#add-user-to-group-form").attr('class').split(' ')[0];
    fetch(`/add-user-group`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: userID,
            group_id: groupID
        })
    })
        .then(response => response.json())
        .then(result => {
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