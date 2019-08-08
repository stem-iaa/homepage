function display_vm_error(error) {
    $(".vm-info").hide();
    $("#vm-alert").text(error);
    $("#vm-error").show();
}

function show_vm_on(ip, port) {
    if (!port) {
        port = "6080";
    }

    $(".vm-info").hide();
    $("#vm-connect-button").attr("href", "http://" + ip + ":" + port + "/vnc.html?host=" + ip + "&port=" + port);
    $("#vm-on").show();
}

function show_vm_off() {
    $(".vm-info").hide();
    $("#vm-off").show();
}

function show_vm_polling() {
    $(".vm-info").hide();
    $("#vm-polling").show();
}

function update_vm_status(timer, until_running) {
    $.ajax({
        url: "/vm/status/" + profile_user,
        type: "get",
        dataType: "json",
        success: function (data) {
            console.log(data);
            if (data.error) {
                clearInterval(timer);
                display_vm_error(data.error);
            } else {
                if (data.status === "running") {
                    clearInterval(timer);
                    $.ajax({
                        url: "/vm/ip/" + profile_user,
                        type: "get",
                        dataType: "json",
                        success: function (data) {
                            console.log(data);
                            if (data.error) {
                                display_vm_error(data.error);
                            } else {
                                show_vm_on(data.ip);
                            }
                        }
                    });
                } else if (data.status === "deallocating") {
                    show_vm_polling();
                } else {
                    if (until_running) {
                        show_vm_polling();
                    } else {
                        clearInterval(timer);
                        show_vm_off();
                    }
                }
            }
        }
    });
}

$(document).ready(function () {
    let timer = window.setInterval(function () {
        update_vm_status(timer);
    }, 2000);
});

$("#start-vm-button").on("click", function () {
    show_vm_polling();
    $.ajax({
        url: "/vm/start/" + profile_user,
        type: "post",
        dataType: "json",
        success: function (data) {
            let timer = window.setInterval(function () {
                update_vm_status(timer, true);
            }, 2000);
        }
    });
});