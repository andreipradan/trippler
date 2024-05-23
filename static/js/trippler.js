$('.modal').on('shown.bs.modal', function () {
  $(this).find('[autofocus]').focus();
});

const setSelectPickerActions = () => {
  $(".actions-btn").removeClass("btn-light")
  $(".bs-actionsbox .btn-group.btn-group-sm").removeClass("btn-group")
}

$('#id_split_with').on('rendered.bs.select', () => {setSelectPickerActions()})
