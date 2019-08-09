$("#cohort-user-search").on("keyup", function () {
    var search_query = $("#cohort-user-search").val();
    if (!search_query) {
        search_query = "";
    }

    $.ajax({
        url: "/cohort/" + cohort_id + "/add_user_search/" + search_query,
        type: "get",
        dataType: "json",
        success: function (data) {
            var html = "";
            for (let i = 0; i < data.length; i++) {
                let user = data[i];
                console.log(user);
                html += `
                <a href="#" class="list-group-item list-group-item-action search-item new-user-link" data-username="${user.username}">
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
            $("#cohort-search-dropdown").html(html);

            $(".new-user-link").on("click", function () {
                let clicked_username = $(this).data("username");
                console.log(clicked_username);
                $.ajax({
                    url: "/cohort/" + cohort_id + "/user/" + clicked_username,
                    type: "post",
                    dataType: "json",
                    success: function (data) {
                        location.reload();
                    }
                });
            });
        }
    });
});

$(".delete-card").on("click", function () {
    let username = $(this).data("id");

    $.ajax({
        url: "/cohort/" + cohort_id + "/user/" + username,
        type: "delete",
        dataType: "json",
        success: function (data) {
            location.reload();
        }
    });
});
