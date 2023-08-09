function deletePatrimonio(patrimonioId) {
  $("#confirmDeleteModal").modal("show");

  $("#confirmDeleteButton").click(() => {
    fetch("/patrimonio-delete", {
      method: "POST",
      body: JSON.stringify({ patrimonioId: patrimonioId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  });
}

