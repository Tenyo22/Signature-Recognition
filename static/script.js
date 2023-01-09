const $comparar = document.querySelector("#btnComparar");

const $canvas = document.querySelector("#canvas");
const contexto = $canvas.getContext("2d");
const COLOR = "black";
const GROSOR = 2;
let xAnterior = 0, yAnterior = 0, xActual = 0, yActual = 0;
const obtenerXReal = (clientX) => clientX - $canvas.getBoundingClientRect().left;
const obtenerYReal = (clientY) => clientY - $canvas.getBoundingClientRect().top;
let haComenzadoDibujo = false; // Bandera que indica si el usuario esta presionando el boton

$canvas.addEventListener("mousedown", evento => {
    // En este evento solo se ha indicado el clic, asi que dibujamos el punto
    xAnterior = xActual;
    yAnterior = yActual;
    xActual = obtenerXReal(evento.clientX);
    yActual = obtenerYReal(evento.clientY);
    contexto.beginPath();
    contexto.fillStyle = COLOR;
    contexto.fillRect(xActual, yActual, GROSOR, GROSOR);
    contexto.closePath();
    // Establecemos la bandera
    haComenzadoDibujo = true;
});

$canvas.addEventListener("mousemove", (evento) => {
    if(!haComenzadoDibujo){
        return;
    }
    // El mouse se esta moviendo y el usuario está presionando el boton, asi que dibujamos
    xAnterior = xActual;
    yAnterior = yActual;
    xActual = obtenerXReal(evento.clientX);
    yActual = obtenerYReal(evento.clientY);
    contexto.beginPath();
    contexto.moveTo(xAnterior, yAnterior);
    contexto.lineTo(xActual, yActual);
    contexto.strokeStyle = COLOR;
    contexto.lineWidth = GROSOR;
    contexto.stroke();
    contexto.closePath();
});
["mouseup", "mouseout"].forEach(nombreDeEvento => {
    $canvas.addEventListener(nombreDeEvento, () => {
        haComenzadoDibujo = false;
    });
})


$comparar.addEventListener("click", function(){
    const dataURI = $canvas.toDataURL();
    localStorage.setItem("firma", dataURI);

    // console.log(dataURI);
    // document.write("img src="+dataURI+"/>");
});