function show1() {
	document.getElementById("caja1").style.display = "block";
	document.getElementById("caja2").style.display = "none";
	document.getElementById("caja3").style.display = "none";
	document.getElementById("caja4").style.display = "none";
}

function show2() {
	document.getElementById("caja1").style.display = "none";
	document.getElementById("caja2").style.display = "block";
	document.getElementById("caja3").style.display = "none";
	document.getElementById("caja4").style.display = "none";
}

function show3() {
	document.getElementById("caja1").style.display = "none";
	document.getElementById("caja2").style.display = "none";
	document.getElementById("caja3").style.display = "block";
	document.getElementById("caja4").style.display = "none";
}

function show4() {
	document.getElementById("caja1").style.display = "none";
	document.getElementById("caja2").style.display = "none";
	document.getElementById("caja3").style.display = "none";
	document.getElementById("caja4").style.display = "block";
}

// PANTALLAS POR SEPARADO
function mostrar1() {
	document.getElementById("caja1").style.display = "block";
	document.getElementById("caja2").style.display = "none";
}

function mostrar2() {
	document.getElementById("caja1").style.display = "none";
	document.getElementById("caja2").style.display = "block";
}

function mostrar3() {
	document.getElementById("caja3").style.display = "block";
	document.getElementById("caja4").style.display = "none";
}

function mostrar4() {
	document.getElementById("caja3").style.display = "none";
	document.getElementById("caja4").style.display = "block";
}
