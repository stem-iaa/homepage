$("#profile-search").on("keyup", function () {
    var search_query = $("#profile-search").val();
    if (!search_query) {
        search_query = "";
    } else {
        search_query += "/8"
    }

    $.ajax({
        url: "/api/search/" + search_query,
        type: "get",
        dataType: "json",
        success: function (data) {
            var html = "";
            for (let i = 0; i < data.length; i++) {
                let user = data[i];
                console.log(user);
                html += `
                <a href="/profile/${user.username}" class="list-group-item list-group-item-action search-item">
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-0">${user.full_name ? user.full_name : user.stylized_username}</h5>
                        <h6 class="m-1">
                            <mark class="user-label-hash text-muted">#</mark><mark class="user-label">${user.label}</mark>
                        </h6>
                    </div>
                    <p class="text-info m-0">${user.full_name ? user.stylized_username : ""}</p>
                </a>
                `;
            }
            $("#search-dropdown").html(html);
        }
    });
});


/*
$(document).ready(function () {
    $(".vm-connect").each(function () {
        console.log($(this).html());
        let this_ = $(this);
        let username = $(this).data("username");
        $.ajax({
            url: "/vm/status/" + username,
            type: "get",
            dataType: "json",
            success: function (data) {
                console.log(data);
                if (data.error) {
                    console.log(data.error);
                    this_.html('');
                } else {
                    if (data.status === "running") {
                        $.ajax({
                            url: "/vm/ip/" + username,
                            type: "get",
                            dataType: "json",
                            success: function (ip_data) {
                                console.log(ip_data);
                                if (ip_data.error) {
                                    this_.html('<div class="alert alert-danger" role="alert" id="vm-alert">\n' + ip_data.error + '</div>')
                                } else {
                                    if (data.status === "running") {
                                        var link = 'http://' + ip_data.ip + ":6080" + "/vnc.html?host=" + ip_data.ip + "&port=6080";
                                        if (ip_data.password) {
                                            link += "&password=" + ip_data.password;
                                        }
                                        this_.html('<a class="btn btn-primary" id="vm-connect-button" href="' +
                                            link +
                                            '" role="button" target="_blank">Connect to VM</a>');
                                    }
                                }
                            }
                        });
                    } else {
                        this_.html('<p>VM is currently <span class="badge badge-danger">stopped</span></p>')
                    }
                }
            }
        });
    });
});
*/
