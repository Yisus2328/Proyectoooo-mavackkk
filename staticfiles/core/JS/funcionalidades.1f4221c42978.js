function confirmarDelete(id) {
    Swal.fire({
        title: "¿Estas seguro?",
        text: "¡No podrás revertir esto!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "¡Sí, bórralo!"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
            title: "¡Eliminado!",
            text: "Su producto ha sido eliminado.",
            icon: "success"
          }).then(function(){
            window.location.href = "/detalle_producto/delete/"+id+"/";
          })
        }
      });
}


