//Modal att

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

//Modal delete

const deleteProfileBtn = document.querySelector('.delete');
const confirmDeleteModal = document.getElementById('confirmDeleteModal');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
const closeModal = document.querySelector('.close');


deleteProfileBtn.addEventListener('click', () => {
  confirmDeleteModal.style.display = 'block';
});


closeModal.addEventListener('click', () => {
  confirmDeleteModal.style.display = 'none';
});


confirmDeleteBtn.addEventListener('click', () => {
  fetch('/excluir_perfil', {
    method: 'POST', 
  })
  .then(response => {
    if (response.redirected) {
      window.location.href = response.url;
    }
  })
  .catch(error => {
    console.error('Erro ao excluir o perfil:', error);
  });
});
