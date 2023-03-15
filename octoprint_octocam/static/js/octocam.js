//used to get cameras connected to your computer
$(() => {
    $("#pull-cameras-button").on("click", (e) => {
        e.preventDefault();
        fetch("http://localhost:8081/getCameras")
            .then(response => {
                return response.json();
            })
            .then(data => {
                cameraList = data;
                // Get a reference to the <select> element
                const selectElem = $('select[name="userCameras"]');
                // Remove any existing options
                selectElem.empty();
                // Loop through the keys in the response object
                Object.keys(cameraList).forEach((cameraName) => {
                    // Create a new <option> element
                    const optionElem = $('<option>', {
                        value: cameraList[cameraName],
                        text: cameraName
                    });
                    // Append the new option to the <select> element
                    selectElem.append(optionElem);
                });
            })
            .catch(error => {
                console.error(error);
                $("#pull-cameras-button").text("Error: " + error.message);
            });
    });
});
//based on the dropdown,width,height values u selected, creates a snapshot and stream url for you
$("#pull-feed-button").on("click",(e)=>{
    e.preventDefault();
    const selectedCameraIndex = $('select[name="userCameras"]').val();
    const width = $('input[name="width"]').val();
    const height = $('input[name="height"]').val();

    const streamUrl="http://localhost:8081/stream/"+selectedCameraIndex+"/"+width+"/"+height;
    const snapshotUrl="http://localhost:8081/snapshot/"+selectedCameraIndex+"/"+width+"/"+height;

    $('#streamUrl').text(streamUrl);
    $('#snapshotUrl').text(snapshotUrl);
});
//used to copy the stream/snapshot url to your clipboard
copyLabelTextToClipboard=(labelId)=>{
    const label = $(`#${labelId}`);
    const tempTextarea = $('<textarea>');
    tempTextarea.val(label.text());
    $('body').append(tempTextarea);
    tempTextarea.select();
    document.execCommand('copy');
    tempTextarea.remove();
}

$('#copyStreamUrl').on("click",(e)=>{
    e.preventDefault();
    copyLabelTextToClipboard('streamUrl');
})
$('#copySnapshotUrl').on("click",(e)=>{
    e.preventDefault();
    copyLabelTextToClipboard('snapshotUrl');
})