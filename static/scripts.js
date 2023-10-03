document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('resultsList').scrollIntoView({
        behavior: 'smooth',
        block: 'center'
    });
});