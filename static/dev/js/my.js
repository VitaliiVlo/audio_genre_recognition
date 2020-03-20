var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];

span.onclick = function () {
    modal.style.display = "none";
};

window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

$("#file-1").change(function () {
    var form = $('#audio_form')[0]; // You need to use standard javascript object here
    var formData = new FormData();
    formData.append('audio', $('input[type=file]')[0].files[0]);
    console.log(formData.get("audio"));
    $("#loader").show();
    $.ajax({
        url: '/recognize',
        data: formData,
        type: 'POST',
        timeout: 0,
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false, // NEEDED, DON'T OMIT THIS
        success: function (data) {
            $("#modal_genre").text(data['genre']);
            modal.style.display = "block";
        },
        complete: function (data) {
            $("#loader").hide();
        }
    });
});
