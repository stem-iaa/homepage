
$("#add-files-button").on("click", function () {
    $("#upload-files-input").click();
});

$("#upload-files-input").on("change", function () {
    if ($("#upload-files-input").get(0).files.length != 0) {
        $("#upload-files-form").submit();
    }
});

$(".file-delete-button").on("click", function() {
    let file_id = $(this).data("file-id");

    $.ajax({
        url: "/solution/file/" + file_id,
        type: "delete",
        dataType: "json",
        success: function (data) {
            location.reload();
        }
    });
});
