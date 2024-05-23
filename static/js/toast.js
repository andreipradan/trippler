(() => {
  'use strict'
  document.querySelectorAll('.toast')
    .forEach(toastNode => {new bootstrap.Toast(toastNode, {autohide: true}).show()})


})
