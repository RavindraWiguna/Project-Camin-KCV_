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


