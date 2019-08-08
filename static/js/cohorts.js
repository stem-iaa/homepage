
function populate_cohorts() {
    let cohort_list = $("#cohort-list");

}

$("#create-cohort-button").on("click", function() {
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

$("#edit-cohort-button").on("click", function() {
    console.log("test");
});
