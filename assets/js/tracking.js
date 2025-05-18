// Script de suivi des clics pour liens d'affiliation
function trackClick(element) {
    // Récupérer les informations du lien
    const product = element.innerText;
    const article = window.location.pathname;
    
    // Préparer les données à envoyer
    const clickData = {
        product: product,
        article: article,
        timestamp: new Date().toISOString(),
        country: navigator.language || navigator.userLanguage,
        device: /Mobi|Android/i.test(navigator.userAgent) ? 'mobile' : 'desktop'
    };
    
    // Envoyer les données au serveur (simulé ici)
    console.log('Click tracked:', clickData);
    
    // Dans une implémentation réelle, on enverrait ces données à un serveur
    // via une requête AJAX ou un pixel de suivi
    
    // On pourrait également stocker temporairement dans localStorage
    try {
        const storedClicks = JSON.parse(localStorage.getItem('affiliate_clicks') || '[]');
        storedClicks.push(clickData);
        localStorage.setItem('affiliate_clicks', JSON.stringify(storedClicks));
    } catch (e) {
        console.error('Error storing click data:', e);
    }
    
    // Ajouter une petite animation pour l'engagement utilisateur
    element.classList.add('clicked');
    setTimeout(() => {
        element.classList.remove('clicked');
    }, 300);
}

// Ajouter styles pour animation de clic
const style = document.createElement('style');
style.textContent = `
.affiliate-link.clicked {
    transform: scale(1.05);
    transition: transform 0.3s ease;
}
`;
document.head.appendChild(style);

// Ajouter suivi automatique pour tous les liens d'affiliation
document.addEventListener('DOMContentLoaded', function() {
    const affiliateLinks = document.querySelectorAll('.affiliate-link');
    affiliateLinks.forEach(link => {
        if (!link.hasAttribute('data-conversion-tracked')) {
            link.setAttribute('data-conversion-tracked', 'true');
            link.addEventListener('click', function() {
                trackClick(this);
            });
        }
    });
});
