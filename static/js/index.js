document.getElementById("tablaFiltro").addEventListener("change", function () {
    const seleccion = this.value;

    if (seleccion === "productos") {
      window.location.href = "/products";
    } else if (seleccion === "clientes") {
      window.location.href = "/home";
    }
  });