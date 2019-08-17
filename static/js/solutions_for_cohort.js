$("#create-solution-button").on("click", function () {
    let solution_name = $("#new-solution-name").val();
    $("#new-solution-name").val("");

    $.ajax({
        url: "/solution",
        type: "post",
        dataType: "json",
        data: {
            "name": solution_name,
            "cohort_id": cohort_id
        },
        success: function (data) {
            if (data.error) {
                alert(data.error);
            } else {
                location.reload();
            }
        }
    });
});

$(".edit-solution-button").on("click", function () {
    let solution_id = $(this).data("solution");
    let solution_link = $("#solution_link_" + solution_id);
    let solution_link_text = solution_link.text();
    solution_link.hide();
    solution_link.parent().prepend(
        "<input type='text' class='form-control col-4' id='solution_name_input_" +
        solution_id +
        "' value='" + solution_link_text + "'></input>"
    );
    $(this).hide();
    $(this).parent().find(".save-solution-button").show();
});

$(".save-solution-button").on("click", function () {
    let solution_id = $(this).data("solution");
    let solution_link = $("#solution_link_" + solution_id);
    let solution_name_input = $("#solution_name_input_" + solution_id);
    let new_solution_name = solution_name_input.val();

    let this_ = $(this);

    $.ajax({
        url: "/solution/" + solution_id,
        type: "post",
        dataType: "json",
        data: {
            "name": new_solution_name
        },
        success: function (data) {
            if (!data.error) {
                solution_link.text(data.name);
                solution_name_input.remove();
                solution_link.show();
                this_.hide();
                this_.parent().find(".edit-solution-button").show();
            }
        }
    });
});

$(".delete-solution-button").on("click", function () {
    let solution_id = $(this).data("solution");

    $.ajax({
        url: "/solution/" + solution_id,
        type: "delete",
        dataType: "json",
        success: function (data) {
            location.reload();
        }
    });
});
