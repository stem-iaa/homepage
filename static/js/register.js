$(document).ready(function () {
    $("#is_student_collapse").collapse("show");
});

$("#is_student_button").on("click", function () {
    $(".user_type_collapse").collapse("hide");
    $("#is_student_collapse").collapse("show");
});

$("#is_mentor_button").on("click", function () {
    $(".user_type_collapse").collapse("hide");
    $("#is_mentor_collapse").collapse("show");
});

$("#is_instructor_button").on("click", function () {
    $(".user_type_collapse").collapse("hide");
    $("#is_instructor_collapse").collapse("show");
});

$("#register-submit-button").on("click", function () {
    let submit_alert = $("#submit-alert");
    let success_alert = $("#submit-success");
    let register_form = $("#register-form");
    submit_alert.hide();
    success_alert.hide();
    $.ajax({
        url: "/register",
        type: "post",
        dataType: "json",
        data: register_form.serialize(),
        success: function (data) {
            if (data.error) {
                submit_alert.text(data.error);
                submit_alert.show();
            } else {
                register_form.trigger("reset");
                success_alert.text(data["info"]["username"] + " created!");
                success_alert.show();
            }
        }
    });
});

