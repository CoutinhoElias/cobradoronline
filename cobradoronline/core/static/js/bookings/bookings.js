$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'post',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-bookings .modal-content").html("");
        $("#modal-bookings").modal("show");
      },
      success: function (data) {
        $("#modal-bookings .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#calendar").html(data.html_book_list);
          $("#modal-bookings").modal("hide");
        }
        else {
          $("#modal-bookings .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-create-book").click(loadForm);
  $("#modal-bookings").on("submit", ".js-book-create-form", saveForm);

  // Update book
  $("#book-table").on("click", ".js-update-book", loadForm);
  $("#modal-bookings").on("submit", ".js-book-update-form", saveForm);

  // Delete book
  $("#book-table").on("click", ".js-delete-book", loadForm);
  $("#modal-bookings").on("submit", ".js-book-delete-form", saveForm);

});
