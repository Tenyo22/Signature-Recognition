var $input = document.getElementById("jsvar");

document.addEventListener("DOMContentLoaded", () => {
    const $recentImage = localStorage.getItem("firma");
    let $text = '{ "key": "'+$recentImage+'"}';
    if($recentImage) {
        document.querySelector("#imgPreview").setAttribute("src", $recentImage);
        // document.querySelector("#jsvar").setAttributes("value", $recentImage);
        $input.value=$recentImage;
        // console.log($input.value);
    }
    // console.log($recentImage);
    // console.log($text);
    $file= dataURItoFile($recentImage, 'prueba.png');
    // console.log($file);
});

function dataURItoFile(dataurl, filename){
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
    bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, {type:mime});
}