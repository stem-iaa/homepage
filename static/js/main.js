$("#profile-search").on("keyup", function () {
    var search_query = $("#profile-search").val();
    if (!search_query) {
        search_query = "";
    }

    $.ajax({
        url: "/search/" + search_query,
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
                                        this_.html('<a class="btn btn-primary" id="vm-connect-button" href="' +
                                            'http://' + ip_data.ip + ":6080" + "/vnc.html?host=" + ip_data.ip + "&port=6080" +
                                            '" role="button" target="_blank">Connect to VM</a>');
                                        $.ajax({
                                            url: "/profile/" + username + "/worm_password",
                                            type: "get",
                                            dataType: "json",
                                            success: function (worm_password_data) {
                                                if (!worm_password_data.error) {
                                                    this_.append('<br>');
                                                    this_.append('<input class="form-control mt-1 form-control-sm" type="text" value="' + worm_password_data.worm_password + '" readonly>');
                                                } else {
                                                    console.log(worm_password_data.error);
                                                }
                                            }
                                        });
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
