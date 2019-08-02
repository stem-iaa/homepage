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
                html += "<div class='search-result' style='padding: 10px;'>";
                html += "<a href='/profile/" + user.username + "'>";
                html += "<h5>" + user.full_name + "</h5>";
                html += "<h6>" + user.stylized_username + "</h6>";
                html += "</a>";
                html += "<hr>";
                html += "</div>";
            }
            $("#search-dropdown").html(html);
        }
    });
});
