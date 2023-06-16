function deletePatrimonio(patrimonioId) {
  $('#confirmDeleteModal').modal('show');

  $('#confirmDeleteButton').click(() => {
    fetch("/delete-patrimonio", {
      method: "POST",
      body: JSON.stringify({ patrimonioId: patrimonioId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  });
}