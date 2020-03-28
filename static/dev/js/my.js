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
    var formData = new FormData();
    var fileInput = $('input[type=file]');
    formData.append('audio', fileInput[0].files[0]);
    var fileExtension = ['.mp3', '.mp3', '.aac', '.oga', '.flac', '.wav', '.pcm', '.aiff', '.wma'];
    if ($.inArray(fileInput.val().split('.').pop().toLowerCase(), fileExtension) === -1) {
        alert("Only formats are allowed : " + fileExtension.join(', '));
        return;
    }
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
