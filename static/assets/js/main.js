// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Track outbound affiliate links (anonymously)
    document.querySelectorAll('a[href^="/go/"]').forEach(link => {
        link.addEventListener('click', function() {
            // You could add analytics here if needed
            console.log('Affiliate link clicked: ' + this.href);
        });
    });
});
