(function () {
    var video = document.getElementById('video'),
        canvas = document.getElementById('canvas'),
        context = canvas.getContext('2d'),
        photo = document.getElementById('photo'),
        vendorUrl = window.URL || window.webkitURL;

    navigator.getMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

    navigator.getMedia({
        video: true,
        audio: false
    }, function (stream) {
            video.srcObject = stream;
            video.play();
    }, function (error) {
        
    });

    document.getElementById('capture').addEventListener('click', function () {
        context.drawImage(video, 0, 0, 400, 300);
        dataURL = canvas.toDataURL('image/png')
        image.setAttribute('src', canvas.toDataURL('image/png'));
        console.log(dataURL)
        $.ajax({
            type: "POST",
            url: "/predict", 
            data:{
                imgBase64: dataURL
            },
            success: function (data) {
                if (data.success) {
                    alert('Your file was successfully uploaded!');
                } else {
                    alert('There was an error uploading your file!');
                }
            },
            error: function (data) {
                alert('There was an error uploading your file!');
            }
        }).done(function () {
            console.log("Sent");
        });
    });
})(); 





