// const image_input = document.querySelector("#img-input");
// var uploaded_image = "";
var constraints = { video: { facingMode: "user" }, audio: false };
// image_input.addEventListener("change", function(){
//     const reader = new FileReader();
//     reader.addEventListener("load", () => {
//         uploaded_image = reader.result;
//         document.querySelector("#display-image").style.backgroundImage = `url(${uploaded_image})`
//     });
//     reader.readAsDataURL(this.files[0]);
// })

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


