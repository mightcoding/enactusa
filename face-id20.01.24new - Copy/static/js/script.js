document.getElementById('startCapture').addEventListener('click', function() {
    let formData = new FormData(document.getElementById('userDataForm'));
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        let video = document.getElementById('video');
        video.srcObject = stream;
        takePictures(formData, stream);
    });
});

function takePictures(formData, stream) {
    let canvas = document.createElement('canvas');
    canvas.width = 640;
    canvas.height = 480;
    let context = canvas.getContext('2d');
    let video = document.getElementById('video');
    video.addEventListener('canplay', function() {
        setTimeout(function() {
            for (let i = 0; i < 20; i++) {
                setTimeout(function() {
                    context.drawImage(video, 0, 0, 640, 480);
                    let imageData = canvas.toDataURL('image/png');
                    let dataToSend = new FormData();
                    for (let key of formData.keys()) {
                        dataToSend.append(key, formData.get(key));
                    }
                    dataToSend.append('imageData', imageData);
                    fetch('/save_image', {
                        method: 'POST',
                        body: dataToSend
                    })
                    .then(response => response.json())
                    .then(data => console.log(data))
                    .catch(error => console.error(error));
                }, i * 1000); // Интервал между снимками
            }
        }, 1000);
    });
}
