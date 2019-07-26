
var original_edit_button;

$(document).ready(function() {
    original_edit_button_text = $("#edit_button")[0]
});

var editing = false;
var editables = {};

$("#edit_button").on("click", function() {
    if (editing) {
        for (var id in editables) {
            $("#" + id).html($("#" + id + " textarea").val());
        }
        editing = false;
    } else {
        $(".editable").each(function() {
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
