// ------------------------------------------------------ //
// For demo purposes, can be deleted
// ------------------------------------------------------ //

$("#page").change(function () {

    if ($(this).val() !== '') {

        window.location.href = $(this).val();

    }

    return false;
});