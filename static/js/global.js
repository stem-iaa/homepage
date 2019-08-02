function getCurrentUser(callback) {
    $.ajax({
        url: "/current_user",
        type: "get",
        dataType: "json",
        success: function (data) {
            callback(data);
        }
    });
}
