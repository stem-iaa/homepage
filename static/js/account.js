
$("#update-button").on("click", function () {
    let submit_alert = $("#settings-submit-alert");
    let success_alert = $("#settings-submit-success");
    let form = $("#account-settings-form");
    submit_alert.hide();
    success_alert.hide();

    $.ajax({
        url: "/profile/" + profile_user + "/update",
        type: "post",
        dataType: "json",
        data: form.serialize(),
        success: function (data) {
            if (data.error) {
                submit_alert.text(data.error);
                submit_alert.show();
            } else {
                window.location.replace("/profile/" + data["info"]["username"] + "/account");
                //success_alert.show();
            }
        }
    });
});

$("#update-password-button").on("click", function () {
    let submit_alert = $("#submit-alert");
    let success_alert = $("#submit-success");
    let form = $("#update-password-form");
    $.ajax({
        url: "/profile/" + profile_user + "/password",
        type: "post",
        dataType: "json",
        data: form.serialize(),
        success: function (data) {
            if (data.error) {
                submit_alert.text(data.error);
                submit_alert.show();
            } else {
                form.trigger("reset");
                success_alert.show();
            }
        }
    });
});
