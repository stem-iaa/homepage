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
                <a href="/profile/${ user.username }" class="list-group-item list-group-item-action search-item">
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-0">${user.full_name ? user.full_name : user.stylized_username}</h5>
                        <h6 class="m-1">
                            <mark class="user-label-hash text-muted">#</mark><mark class="user-label">${ user.label }</mark>
                        </h6>
                    </div>
                    <p class="text-info m-0">${ user.full_name ? user.stylized_username : "" }</p>
                </a>
                `;
            }
            $("#search-dropdown").html(html);
        }
    });
});
