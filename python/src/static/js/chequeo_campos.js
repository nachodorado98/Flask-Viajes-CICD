document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("formulario");
    const boton = document.getElementById("btn-submit");

    function validarFormulario() {
        boton.disabled = !form.checkValidity();
    }

    form.addEventListener("input", validarFormulario);

    validarFormulario();
});