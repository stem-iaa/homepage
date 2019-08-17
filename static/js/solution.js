
$("#add-files-button").on("click", function () {
    $("#upload-files-input").click();
});

$("#upload-files-input").on("change", function () {
    if ($("#upload-files-input").get(0).files.length != 0) {
        $("#upload-files-form").submit();
    }
});
