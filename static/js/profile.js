var original_edit_button_text;

$(document).ready(function () {
    original_edit_button_text = $("#edit_button").text();
});

var editing = false;
var editables = {};

$("#edit_button").on("click", function () {
    if (editing) {
        var editable_content = {};
        for (var id in editables) {
            editable_content[id] = $("#" + id + " textarea").val();
        }

        $.ajax({
            url: "/profile/" + profile_user + "/update",
            type: "post",
            dataType: "json",
            data: editable_content,
            success: function (data) {
                if (!data.error) {
                    location.reload();

                }
            }
        });
    } else {
        $(".editable").each(function () {
            editables[this.id] = this;
            let current_html = $(this).html();
            $(this).html("<textarea style='width: 100%;'>" + current_html + "</textarea>");
            let textarea = $("#" + this.id + " textarea")[0];
            textarea.style.height = textarea.scrollHeight + 5 + "px";
        });
        editing = true;
        $("#edit_button").text("Save");
    }

});
