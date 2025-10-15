document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-viaje");
    const boton = document.getElementById("btn-submit");

    function validarFormulario() {
        const valido = form.checkValidity();
        boton.disabled = !valido;

        if (boton.disabled) {
            boton.style.opacity = "0.6";
            boton.style.cursor = "not-allowed";
        } else {
            boton.style.opacity = "1";
            boton.style.cursor = "pointer";
        }
    }

    ["input", "change", "blur"].forEach(evt => {
        form.addEventListener(evt, validarFormulario, true);
    });

    validarFormulario();
});
