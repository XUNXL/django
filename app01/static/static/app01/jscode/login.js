let currentUrl = window.location.href;
function turnTOAdmin() {
    document.querySelector('.logo').addEventListener('dblclick', function () {
        window.location.href = '../adminlogin/';
    });
}
turnTOAdmin();
