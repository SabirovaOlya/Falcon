document.addEventListener('DOMContentLoaded', function () {
    const categorySpans = document.querySelectorAll('.nav-link-text');

    categorySpans.forEach(span => {
        span.addEventListener('click', function (event) {
            const url = this.getAttribute('data-url');
            window.location.href = url;
        });
    });
});

console.log('connect')