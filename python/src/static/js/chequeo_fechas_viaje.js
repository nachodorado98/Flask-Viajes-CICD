document.addEventListener('DOMContentLoaded', function () {
  const ida = document.getElementById('fecha-ida');
  const vuelta = document.getElementById('fecha-vuelta');
  const form = document.querySelector('form');

  function parseYMD(value) {
    if (!value) return null;
    const [y, m, d] = value.split('-').map(Number);
    return new Date(y, m - 1, d);
  }

  function validarFechas() {
    const fIda = parseYMD(ida.value);
    const fVuelta = parseYMD(vuelta.value);

    if (!fIda || !fVuelta) {
      vuelta.setCustomValidity('');
      return;
    }

    if (fIda > fVuelta) {
      vuelta.setCustomValidity("La fecha de vuelta no puede ser anterior a la de ida");
    } else {
      vuelta.setCustomValidity("");
    }
  }

  function actualizarMinVuelta(autocorregir = true) {
    if (ida.value) {
      vuelta.min = ida.value;
      if (vuelta.value) {
        const fIda = parseYMD(ida.value);
        const fVuelta = parseYMD(vuelta.value);
        if (fVuelta < fIda) {
          if (autocorregir) {
            vuelta.value = ida.value;
            vuelta.setCustomValidity("");
          } else {
            vuelta.setCustomValidity("La fecha de vuelta no puede ser anterior a la de ida");
          }
        }
      }
    } else {
      vuelta.removeAttribute('min');
    }
    validarFechas();
  }

  ida.addEventListener('input', () => actualizarMinVuelta(true));
  vuelta.addEventListener('input', validarFechas);

  form.addEventListener('submit', (e) => {
    validarFechas();
    if (!form.checkValidity()) {
      e.preventDefault();
      form.reportValidity();
    }
  });

  actualizarMinVuelta(false);
});