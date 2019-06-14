$('#DeleteRecordModal').on('show.bs.modal', function(e) {
    $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
});

// $('#SendEmailWithSoftwareUpdateModal').on('show.bs.modal', function(e) {
//     $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
// });