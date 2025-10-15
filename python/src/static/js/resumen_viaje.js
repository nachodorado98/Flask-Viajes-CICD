document.addEventListener("DOMContentLoaded", () => {
    
    const form = document.getElementById("form-viaje");
    const modal = document.getElementById("resumen-modal");
    const cerrarModal = document.getElementById("cerrar-modal");
    const resumenDetalle = document.getElementById("resumen-detalle");
    const btnConfirmar = document.getElementById("confirmar");
    const btnEditar = document.getElementById("editar");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const transporteSelect = form.transporte;
        const transporteTexto = transporteSelect.options[transporteSelect.selectedIndex].text;
        const transporteValor = transporteSelect.value;

        const datos = {
            pais: form.pais.value.trim(),
            ciudad: form.ciudad.value.trim(),
            fechaIda: form["fecha-ida"].value,
            fechaVuelta: form["fecha-vuelta"].value,
            hotel: form.hotel.value.trim(),
            web: form.web.value.trim(),
            transporteTexto: transporteTexto,
            transporteValor: transporteValor,
            comentario: form.comentario.value.trim()
        };

        if (!datos.hotel) datos.hotel = "No especificado";
        if (!datos.web) datos.web = "No indicada";
        if (!datos.comentario) datos.comentario = "Sin comentarios";

        resumenDetalle.innerHTML = `
            <div class="resumen-item">
                <span class="resumen-label">País</span>
                <span class="resumen-valor">${datos.pais}</span>
            </div>
            <div class="resumen-item">
                <span class="resumen-label">Ciudad</span>
                <span class="resumen-valor">${datos.ciudad}</span>
            </div>
            <div class="resumen-item">
                <span class="resumen-label">Fecha de ida</span>
                <span class="resumen-valor">${datos.fechaIda}</span>
            </div>
            <div class="resumen-item">
                <span class="resumen-label">Fecha de vuelta</span>
                <span class="resumen-valor">${datos.fechaVuelta}</span>
            </div>
            <div class="resumen-item">
                <span class="resumen-label">Hotel</span>
                <span class="resumen-valor">${datos.hotel}</span>
            </div>
            <div class="resumen-item">
                <span class="resumen-label">Web</span>
                <span class="resumen-valor">${datos.web}</span>
            </div>
            <div class="resumen-item">
                <span class="resumen-label">Transporte</span>
                <span class="resumen-valor">${datos.transporteTexto}</span>
            </div>
            <div class="resumen-item" style="grid-column: 1 / -1;">
                <span class="resumen-label">Comentario</span>
                <div class="resumen-comentario">${datos.comentario}</div>
            </div>
        `;

        modal.style.display = "block";
    });

    cerrarModal.onclick = () => modal.style.display = "none";
    btnEditar.onclick = () => modal.style.display = "none";
    window.onclick = (e) => { if (e.target === modal) modal.style.display = "none"; }

    btnConfirmar.onclick = () => {
        console.log("Acción pendiente de implementar");
    };

});