
function startUpdate(){
    data="this is the data from java script"
    var request = new XMLHttpRequest();
    request.addEventListener('load', function(event) {
        if (request.status >= 200 && request.status < 300) {
            document.getElementById("auto-update-box").innerHTML = this.responseText;

            console.log(request.responseText);
        } else {
            console.warn(request.statusText, request.responseText);
        }
        setTimeout(startUpdate, 1000)
    });

    request.open("POST","/");
    request.send(data);

}