function populate_cohorts() {
    let cohort_list = $("#cohort-list");

}

$("#create-cohort-button").on("click", function () {
    let cohort_name = $("#new-cohort-name").val();
    $("#new-cohort-name").val("");

    $.ajax({
        url: "/cohort",
        type: "post",
        dataType: "json",
        data: {
            "name": cohort_name
        },
        success: function (data) {
            location.reload();
        }
    });
});

$(".edit-cohort-button").on("click", function () {
    let cohort_id = $(this).data("cohort");
    let cohort_link = $("#cohort_link_" + cohort_id);
    let cohort_link_text = cohort_link.text();
    cohort_link.hide();
    cohort_link.parent().prepend(
        "<input type='text' class='form-control col-4' id='cohort_name_input_" +
        cohort_id +
        "' value='" + cohort_link_text + "'></input>"
    );
    $(this).hide();
    $(this).parent().find(".save-cohort-button").show();
});

$(".save-cohort-button").on("click", function () {
    let cohort_id = $(this).data("cohort");
    let cohort_link = $("#cohort_link_" + cohort_id);
    let cohort_name_input = $("#cohort_name_input_" + cohort_id);
    let new_cohort_name = cohort_name_input.val();

    let this_ = $(this);

    $.ajax({
        url: "/cohort/" + cohort_id,
        type: "post",
        dataType: "json",
        data: {
            "name": new_cohort_name
        },
        success: function (data) {
            if (!data.error) {
                cohort_link.text(data.name);
                cohort_name_input.remove();
                cohort_link.show();
                this_.hide();
                this_.parent().find(".edit-cohort-button").show();
            }
        }
    });
});

$(".delete-cohort-button").on("click", function () {
    let cohort_id = $(this).data("cohort");

    $.ajax({
        url: "/cohort/" + cohort_id,
        type: "delete",
        dataType: "json",
        success: function (data) {
            location.reload();
        }
    });
});

$(".cohort-active-checkbox").on("click", function () {
    let cohort_id = $(this).data("cohort");

    $.ajax({
        url: "/cohort/" + cohort_id,
        type: "post",
        dataType: "json",
        data: {
            "is_active": $(this).prop("checked")
        },
        success: function (data) {
            if (!data.error) {
                $(this).prop("checked", data.is_active);
            }
        }
    });
});
