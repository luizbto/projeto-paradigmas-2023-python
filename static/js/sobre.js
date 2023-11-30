document.addEventListener("DOMContentLoaded", function() {
    const dropdowns = document.querySelectorAll('.common-dropdown');

    dropdowns.forEach(dropdown => {
        const dropdownContent = dropdown.querySelector('.dropdown-content');
        const svgIcon = dropdown.querySelector('svg');

        svgIcon.addEventListener('click', (event) => {
            event.preventDefault();
            dropdownContent.classList.toggle('show');
        });

        window.addEventListener('click', event => {
            if (!event.target.closest('.common-dropdown')) {
                dropdownContent.classList.remove('show');
            }
        });
    });
});