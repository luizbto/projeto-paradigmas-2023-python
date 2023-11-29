$(document).ready(function() {
    $('#confirmUpdateBtn').click(function(event) {
        event.preventDefault();

        $('#confirmModal').css('display', 'block');
        
        setTimeout(function() {
            $('#confirmModal').css('display', 'none');
        }, 200000);
    });

    $('.close').click(function() {
        $('#confirmModal').css('display', 'none');
    });

    $(window).click(function(event) {
        if (event.target == document.getElementById('confirmModal')) {
            $('#confirmModal').css('display', 'none');
        }
    });
});