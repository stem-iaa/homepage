function getCurrentUser(callback) {
    $.ajax({
        url: "/current_user",
        type: "get",
        dataType: "json",
        success: function (data) {
            callback(data);
        }
    });
}

$('a[href*="#"]').on('click', function (e) {
    e.preventDefault();

    $('html, body').animate(
        {
            scrollTop: $($(this).attr('href')).offset().top,
        },
        400,
        'swing'
    );
});
