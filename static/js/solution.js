var original_edit_button_text;

var quill;
var editing = false;

$(document).ready(function () {
    original_edit_button_text = $("#edit-description-button").text();

    quill = new Quill('#description', {
        theme: 'snow'
    });
    quill.enable(false);
    $(".ql-toolbar").hide();
});

$("#edit-description-button").on("click", function () {
    if (editing) {
        $.ajax({
            url: "/solution/" + solution_id + "/description",
            type: "post",
            dataType: "json",
            data: {
                "description": $("#description").html()
            },
            success: function (data) {
                if (!data.error) {
                    quill.enable(false);
                    $(".ql-toolbar").hide();
                    $("#edit-description-button").text(original_edit_button_text);

                    editing = false;
                }
            }
        });
    } else {
        quill.enable(true);
        $(".ql-toolbar").show();
        $("#edit-description-button").text("Save");

        editing = true;
    }
});

$("#add-files-button").on("click", function () {
    $("#upload-files-input").click();
});

$("#upload-files-input").on("change", function () {
    if ($("#upload-files-input").get(0).files.length != 0) {
        $("#upload-files-form").submit();
    }
});

$(".file-delete-button").on("click", function () {
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
