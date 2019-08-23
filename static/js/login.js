
$("#login-submit-button").on("click", function () {
    let submit_alert = $("#submit-alert");
    let success_alert = $("#submit-success");
    let login_form = $("#login-form");
    submit_alert.hide();
    success_alert.hide();
    $.ajax({
        url: "/login",
        type: "post",
        dataType: "json",
        data: login_form.serialize(),
        success: function (data) {
            if (data.error) {
                submit_alert.text(data.error);
                submit_alert.show();
            } else {
                window.location.replace(data.location);
            }
        }
    });
});

$(document).on('keypress',function(e) {
    if(e.which === 13) {
        $("#login-submit-button").click();
    }
});
