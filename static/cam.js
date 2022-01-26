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

//===========================MAIN FUNC=======================
//make a socket object
var socket = io();
socket.on('connect', function(){
    console.log("Connected...!", socket.connected)
});

//get video, image, and camera button element
const video_element = document.querySelector("#videoElement");
const image_id = document.querySelector('#camera-output');
const startCamBtn = document.querySelector("#start-cam");
const stopCamBtn = document.querySelector("#stop-cam");
const changeCamBtn = document.querySelector("#change-cam");

// Set constraints for the video stream
const constraints0 = { video: { facingMode: "user" }, audio: false };
const constraints1 = { video: { facingMode: "environment" }, audio: false };
const configList = [constraints0, constraints1];
var idConfig = 0;

//Camera Triggers Util
if(!!stopCamBtn){
    stopCamBtn.addEventListener('click', function(){
        // alert("going to '' ");
        location.href = "/";
        
    });
}

if(!!startCamBtn){
    startCamBtn.addEventListener('click', function(){
        // alert("starting camera");
        location.href = "/detect";
    });
}

if(!!changeCamBtn){
    changeCamBtn.addEventListener('click', function(){
        idConfig++;
        idConfig %= 2;
        cameraStart();

        shootFirstFrameHandler();
    
    });
}

// Access the device camera and stream to cameraView
function cameraStart() {
    navigator.mediaDevices
        .getUserMedia(configList[idConfig])
        .then(function(stream) {
        // track = stream.getTracks()[0];
        video_element.srcObject = stream;
    })
    .catch(function(error) {
        console.error("Oops. Something is broken.", error);
    });
}

function shootFirstFrameHandler(){
    let x = 12;
    let interval = 500;
    let isNotStart = true;
    let type = "image/webp";
    for (var i = 0; i < x && isNotStart; i++) {
        setTimeout(function () {
        let frame = capture(video_element, 0.625);
        let data = frame.toDataURL(type);
        data = data.replace('data:image/webp;base64,', '');
        if(!(data.includes("data"))){
            socket.emit('image', data);
            isNotStart=false;//break out of the loop
            console.log("not null");
            // console.log(data);
            // alert(data);
        }else{
            console.log("data null");
        }
        }, i * interval)
    }
}

//if exist video, then gas
if(!!video_element){
    video_element.style.display = "none";
    // const FPS = 5;
    const type = "image/webp";

    cameraStart();

    shootFirstFrameHandler();

    //ready to process
    // setInterval(function(){

    // }, 1000/FPS);
    // Set a function to run every "interval" seconds a total of "x" times

    socket.on('response_back', function(image){        
        image_id.src = image;
        let frame = capture(video_element, 0.5);
        let data = frame.toDataURL(type);
        data = data.replace('data:image/webp;base64,', '');
        socket.emit('image', data);        
    });
}


