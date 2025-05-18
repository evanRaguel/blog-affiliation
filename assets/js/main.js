/**
 * Fichier JavaScript principal pour le blog d'affiliation
 * Contient les fonctions communes à toutes les pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling pour les ancres
    initSmoothScrolling();
    
    // Suivi des liens d'affiliation
    trackAffiliateLinks();
    
    // Mettre en évidence les liens d'affiliation pour attirer l'attention
    highlightAffiliateLinks();
    
    // Ajouter badges de prix aux produits
    addPriceBadges();
    
    // Initialiser les tableaux comparatifs interactifs
    initComparisonTables();
    
    // Ajouter des statistiques de confiance aux produits
    addTrustStatistics();
    
    // Ajouter gestion des commentaires des utilisateurs
    initComments();
    
    // Initialiser la barre de progression de lecture
    initReadingProgressBar();
    
    // Ajouter bannière de temps limité
    addTimeLimitedBanner();
});

/**
 * Initialise le smooth scrolling pour les ancres
 */
function initSmoothScrolling() {
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
}

/**
 * Suit les clics sur les liens d'affiliation
 */
function trackAffiliateLinks() {
    document.querySelectorAll('a[href^="/go/"]').forEach(link => {
        link.addEventListener('click', function() {
            // Vous pourriez ajouter ici des analytics plus avancés
            console.log('Affiliate link clicked: ' + this.href);
            
            try {
                // Enregistrer dans localStorage pour demo
                const clicks = JSON.parse(localStorage.getItem('affiliate_clicks') || '[]');
                clicks.push({
                    link: this.href,
                    text: this.textContent,
                    timestamp: new Date().toISOString(),
                    page: window.location.pathname
                });
                localStorage.setItem('affiliate_clicks', JSON.stringify(clicks));
            } catch (e) {
                console.error('Error storing click:', e);
            }
            
            // Envoyer à Google Analytics
            if (typeof gtag === 'function') {
                gtag('event', 'click', {
                    'event_category': 'Affiliate Link',
                    'event_label': this.textContent,
                    'value': 1
                });
            }
        });
    });
}

/**
 * Met en évidence les liens d'affiliation pour attirer l'attention
 */
function highlightAffiliateLinks() {
    const affiliateLinks = document.querySelectorAll('a[href^="/go/"]');
    affiliateLinks.forEach(link => {
        link.classList.add('highlight');
        
        // Ajouter icône de panier à côté du lien pour suggérer l'achat
        if (!link.querySelector('.cart-icon')) {
            const cartIcon = document.createElement('span');
            cartIcon.className = 'cart-icon';
            cartIcon.innerHTML = ' 🛒';
            cartIcon.style.fontSize = '0.9em';
            link.appendChild(cartIcon);
        }
    });
}

/**
 * Ajoute des badges de prix avec des réductions
 */
function addPriceBadges() {
    const productBoxes = document.querySelectorAll('.product-box, .recommended-product');
    productBoxes.forEach((box, index) => {
        if (!box.querySelector('.price-tag')) {
            // Simuler des discounts variés
            const discounts = [10, 15, 20, 25, 30];
            const discount = discounts[Math.floor(Math.random() * discounts.length)];
            
            // Générer des prix réalistes
            const basePrice = Math.floor(50 + Math.random() * 150);
            const discountedPrice = Math.round((basePrice * (100 - discount)) / 100);
            
            // Créer la balise de prix
            const priceTag = document.createElement('div');
            priceTag.className = 'price-tag';
            priceTag.innerHTML = `
                <span class="old-price">${basePrice},99€</span>
                <span class="new-price">${discountedPrice},99€</span>
                <span class="discount-percent">-${discount}%</span>
            `;
            
            // Insérer après le titre
            const title = box.querySelector('h3');
            if (title) {
                title.insertAdjacentElement('afterend', priceTag);
            } else {
                box.prepend(priceTag);
            }
        }
    });
}

/**
 * Initialise les tableaux comparatifs interactifs
 */
function initComparisonTables() {
    const tables = document.querySelectorAll('.comparison-table');
    tables.forEach(table => {
        // Ajouter une classe pour le tri
        table.classList.add('sortable');
        
        // Ajouter des indicateurs pour le tri dans les entêtes
        const headers = table.querySelectorAll('th');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(this);
            });
            
            // Ajouter un indicateur de tri
            if (!header.querySelector('.sort-indicator')) {
                const sortIndicator = document.createElement('span');
                sortIndicator.className = 'sort-indicator';
                sortIndicator.textContent = ' ↕️';
                header.appendChild(sortIndicator);
            }
        });
    });
}

/**
 * Trie un tableau en fonction de la colonne cliquée
 */
function sortTable(header) {
    const table = header.closest('table');
    const tbody = table.querySelector('tbody');
    if (!tbody) return;
    
    const rows = Array.from(tbody.rows);
    const columnIndex = Array.from(header.parentNode.cells).indexOf(header);
    
    // Déterminer l'ordre de tri
    const ascending = header.getAttribute('data-sort') !== 'asc';
    header.setAttribute('data-sort', ascending ? 'asc' : 'desc');
    
    // Mettre à jour l'indicateur de tri
    const indicator = header.querySelector('.sort-indicator');
    if (indicator) {
        indicator.textContent = ascending ? ' ↑' : ' ↓';
    }
    
    // Trier les lignes
    rows.sort((a, b) => {
        const cellA = a.cells[columnIndex].textContent.trim();
        const cellB = b.cells[columnIndex].textContent.trim();
        
        // Essayer de trier comme des nombres si possible
        const numA = parseFloat(cellA);
        const numB = parseFloat(cellB);
        
        if (!isNaN(numA) && !isNaN(numB)) {
            return ascending ? numA - numB : numB - numA;
        }
        
        // Sinon, trier comme du texte
        return ascending 
            ? cellA.localeCompare(cellB, 'fr') 
            : cellB.localeCompare(cellA, 'fr');
    });
    
    // Réorganiser le tableau
    rows.forEach(row => tbody.appendChild(row));
}

/**
 * Ajoute des statistiques de confiance aux produits
 */
function addTrustStatistics() {
    const productBoxes = document.querySelectorAll('.recommended-product');
    productBoxes.forEach(box => {
        if (!box.querySelector('.trust-stats')) {
            // Créer les statistiques de confiance
            const stats = document.createElement('div');
            stats.className = 'trust-stats';
            
            // Générer des nombres réalistes
            const views = Math.floor(1000 + Math.random() * 9000);
            const purchases = Math.floor(views * (0.05 + Math.random() * 0.15));
            
            stats.innerHTML = `
                <div class="trust-item">
                    <span class="trust-icon">👁️</span>
                    <span class="trust-value">${views}+ personnes</span>
                    <span class="trust-label">ont consulté ce produit ce mois-ci</span>
                </div>
                <div class="trust-item">
                    <span class="trust-icon">🛒</span>
                    <span class="trust-value">${purchases}+ acheteurs</span>
                    <span class="trust-label">satisfaits</span>
                </div>
                <div class="trust-item">
                    <span class="trust-icon">⚡</span>
                    <span class="trust-label">Expédition rapide sous 24h</span>
                </div>
            `;
            
            // Insérer à la fin de la boîte
            box.appendChild(stats);
        }
    });
}

/**
 * Initialise le système de commentaires
 */
function initComments() {
    const commentSection = document.querySelector('.comments-section');
    if (!commentSection) return;
    
    const form = commentSection.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Récupérer les valeurs
            const nameInput = this.querySelector('input[name="name"]');
            const commentInput = this.querySelector('textarea[name="comment"]');
            
            if (nameInput && commentInput && nameInput.value && commentInput.value) {
                // Créer le commentaire
                const comment = document.createElement('div');
                comment.className = 'comment';
                
                const date = new Date();
                const formattedDate = `${date.getDate()}/${date.getMonth()+1}/${date.getFullYear()}`;
                
                comment.innerHTML = `
                    <div class="comment-header">
                        <span class="comment-author">${nameInput.value}</span>
                        <span class="comment-date">${formattedDate}</span>
                    </div>
                    <div class="comment-content">
                        <p>${commentInput.value}</p>
                    </div>
                    <div class="comment-actions">
                        <button class="comment-like">👍 J'aime</button>
                        <button class="comment-reply">Répondre</button>
                    </div>
                `;
                
                // Ajouter au début de la liste des commentaires
                const commentsList = commentSection.querySelector('.comments-list');
                if (commentsList) {
                    commentsList.prepend(comment);
                }
                
                // Réinitialiser le formulaire
                nameInput.value = '';
                commentInput.value = '';
                
                // Message de confirmation
                alert('Merci pour votre commentaire !');
            }
        });
    }
}

/**
 * Initialise la barre de progression de lecture
 */
function initReadingProgressBar() {
    // Vérifier si l'élément existe déjà
    if (!document.getElementById('progressBar')) {
        // Si nous sommes sur un article (détection basique)
        if (document.querySelector('.post')) {
            // Créer la barre de progression
            const progressContainer = document.createElement('div');
            progressContainer.className = 'progress-container';
            
            const progressBar = document.createElement('div');
            progressBar.className = 'progress-bar';
            progressBar.id = 'progressBar';
            
            progressContainer.appendChild(progressBar);
            document.body.prepend(progressContainer);
            
            // Mettre à jour la barre lors du défilement
            window.addEventListener('scroll', function() {
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = (winScroll / height) * 100;
                progressBar.style.width = scrolled + "%";
            });
        }
    }
}

/**
 * Ajoute une bannière d'offre à durée limitée
 */
function addTimeLimitedBanner() {
    // S'assurer qu'on est sur une page de produit
    if (document.querySelector('.post-content a[href^="/go/"]')) {
        if (!document.querySelector('.time-limited-offer')) {
            // Créer la bannière
            const banner = document.createElement('div');
            banner.className = 'time-limited-offer';
            
            // Date de fin (aujourd'hui + 2 jours)
            const endDate = new Date();
            endDate.setDate(endDate.getDate() + 2);
            
            banner.innerHTML = `
                <div class="offer-content">
                    <span class="offer-tag">OFFRE SPÉCIALE</span>
                    <h4>Remise exclusive de 20% !</h4>
                    <p>Offre limitée, se termine le ${endDate.toLocaleDateString('fr-FR')}</p>
                    <div class="countdown" data-end="${endDate.toISOString()}">
                        <span class="time-unit"><span class="time-value">--</span>h</span>
                        <span class="time-unit"><span class="time-value">--</span>m</span>
                        <span class="time-unit"><span class="time-value">--</span>s</span>
                    </div>
                </div>
            `;
            
            // Trouver un endroit stratégique pour l'ajouter
            const firstParagraph = document.querySelector('.post-content p');
            if (firstParagraph && firstParagraph.parentNode) {
                firstParagraph.parentNode.insertBefore(banner, firstParagraph.nextSibling);
                
                // Lancer le compte à rebours
                startCountdown();
            }
        }
    }
}

/**
 * Gère le compte à rebours des offres limitées
 */
function startCountdown() {
    const countdowns = document.querySelectorAll('.countdown');
    countdowns.forEach(countdown => {
        const endTime = new Date(countdown.getAttribute('data-end')).getTime();
        
        // Mettre à jour toutes les secondes
        const countdownInterval = setInterval(function() {
            // Calculer le temps restant
            const now = new Date().getTime();
            const timeLeft = endTime - now;
            
            if (timeLeft <= 0) {
                // Fin du compte à rebours
                clearInterval(countdownInterval);
                countdown.innerHTML = '<span class="expired">Offre expirée</span>';
                return;
            }
            
            // Calculer heures, minutes et secondes
            const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
            
            // Mettre à jour l'affichage
            const timeUnits = countdown.querySelectorAll('.time-value');
            if (timeUnits.length === 3) {
                timeUnits[0].textContent = String(hours).padStart(2, '0');
                timeUnits[1].textContent = String(minutes).padStart(2, '0');
                timeUnits[2].textContent = String(seconds).padStart(2, '0');
            }
        }, 1000);
    });
}
