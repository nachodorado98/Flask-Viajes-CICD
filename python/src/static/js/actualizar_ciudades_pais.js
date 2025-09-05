function actualizarCiudades() {
    
    const paisSeleccionado = document.getElementById("pais").value;
    const listaCiudades = document.getElementById("lista-ciudades");
    const ciudadInput = document.getElementById("ciudad");

    ciudadInput.value = "";

    listaCiudades.innerHTML = "";

    if (paisSeleccionado) {
        fetch("/ciudades_pais?pais=" + encodeURIComponent(paisSeleccionado))
            .then(response => response.json())
            .then(ciudades => {
                ciudades.forEach(function(ciudad) {
                    const option = document.createElement("option");
                    option.value = ciudad;
                    listaCiudades.appendChild(option);
                });
            })
            .catch(error => console.error("Error al obtener ciudades:", error));
    }
}