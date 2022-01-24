//Camera Triggers Util
const stopCamButton = document.getElementById("stop-cam");
if(!!stopCamButton){
    stopCamButton.addEventListener('click', function(){
        // alert("going to '' ");
        location.href = "/";
        
    })
}

const startCamButton = document.getElementById("start-cam");
if(!!startCamButton){
    startCamButton.addEventListener('click', function(){
        // alert("starting camera");
        location.href = "/detect";
    })
}

//Video Function
/**
 * Captures a image frame from the provided video element.
 *
 * @param {Video} video HTML5 video element from where the image frame will be captured.
 * @param {Number} scaleFactor Factor to scale the canvas element that will be return. This is an optional parameter.
 *
 * @return {Canvas}
 */
 function capture(video, scaleFactor) {
    if(scaleFactor == null){
        scaleFactor = 1;
    }
    var w = video.videoWidth * scaleFactor;
    var h = video.videoHeight * scaleFactor;
    var canvas = document.createElement('canvas');
        canvas.width  = w;
        canvas.height = h;
    var ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, w, h);
    return canvas;
}     
 
// /**
//  * Invokes the <code>capture</code> function and attaches the canvas element to the DOM.
//  */
// function shoot(){
//     var video  = document.getElementById(videoId);
//     var output = document.getElementById('output');
//     var canvas = capture(video, scaleFactor);
//         canvas.onclick = function(){
//             window.open(this.toDataURL());
//         };
//     snapshots.unshift(canvas);
//     output.innerHTML = '';
//     for(var i=0; i<4; i++){
//         output.appendChild(snapshots[i]);
//     }
// }

//===========================MAIN FUNC=======================
//make a socket object
var socket = io('http://127.0.0.1:5000');
socket.on('connect', function(){
    console.log("Connected...!", socket.connected)
});

//get video element
const video_element = document.querySelector("#videoElement");
const image_id = document.querySelector('#camera-output');

// Set constraints for the video stream
var constraints = { video: { facingMode: "user" }, audio: false };
// Access the device camera and stream to cameraView
function cameraStart() {
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function(stream) {
        // track = stream.getTracks()[0];
        video_element.srcObject = stream;
    })
    .catch(function(error) {
        console.error("Oops. Something is broken.", error);
    });
}
if(!!video_element){
    video_element.style.display = "none";
    cameraStart();
    const FPS = 20;
    const type = "image/webp";
    //ready to process
    setInterval(function(){
        let frame = capture(video_element, 0.5);
        let data = frame.toDataURL(type);
        data = data.replace('data:' + type + ';base64,', '');
        socket.emit('image', data);
    }, 1000/FPS);

    socket.on('response_back', function(image){        
        image_id.src = image;
    });
}


