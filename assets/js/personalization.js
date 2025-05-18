
// Personnalisation Module
const Personalization = {
    // ID du visiteur
    visitorId: null,
    
    // Profil utilisateur
    userProfile: null,
    
    // Règles de personnalisation
    rules: {"home": {"home_tech_banner": {"id": "home_tech_banner", "segment_id": "tech_enthusiasts", "content_type": "banner", "content": "D\u00e9couvrez nos derni\u00e8res innovations tech avec 15% de r\u00e9duction!", "created_at": "2025-05-17T20:27:22.291695"}, "home_mobile_cta": {"id": "home_mobile_cta", "segment_id": "mobile_users", "content_type": "cta_text", "content": "ACHETER EN 1-CLIC SUR MOBILE", "created_at": "2025-05-17T20:27:22.292303"}}, "article": {"article_tech_products": {"id": "article_tech_products", "segment_id": "tech_enthusiasts", "content_type": "recommended_products", "content": [{"name": "UltraBook Pro X7", "price": "899,99\u20ac", "slug": "ultrabook-pro-x7"}, {"name": "\u00c9couteurs NoiseCancel X5", "price": "149,99\u20ac", "slug": "ecouteurs-noisecancel-x5"}, {"name": "Batterie Externe 20000mAh", "price": "49,99\u20ac", "slug": "batterie-externe-20000mah"}], "created_at": "2025-05-17T20:27:22.293061"}, "article_repeating_visitor": {"id": "article_repeating_visitor", "segment_id": "repeat_visitors", "content_type": "email_capture", "content": {"title": "Bienvenue \u00e0 nouveau!", "text": "Abonnez-vous \u00e0 notre newsletter pour recevoir des offres exclusives r\u00e9serv\u00e9es \u00e0 nos lecteurs fid\u00e8les.", "button": "RECEVOIR -20% SUR VOTRE PROCHAIN ACHAT"}, "created_at": "2025-05-17T20:27:22.293795"}, "article_converted_cta": {"id": "article_converted_cta", "segment_id": "converted_users", "content_type": "cta_text", "content": "ACHETER \u00c0 NOUVEAU AVEC 10% DE R\u00c9DUCTION", "created_at": "2025-05-17T20:27:22.294631"}}},
    
    // Segments
    segments: {"tech_enthusiasts": {"id": "tech_enthusiasts", "name": "Passionn\u00e9s de technologie", "criteria": {"interests": ["technologie", "gadgets", "innovation"], "min_visits": 2}, "created_at": "2025-05-17T20:27:22.289865"}, "mobile_users": {"id": "mobile_users", "name": "Utilisateurs mobiles", "criteria": {"device_type": "mobile"}, "created_at": "2025-05-17T20:27:22.290510"}, "repeat_visitors": {"id": "repeat_visitors", "name": "Visiteurs r\u00e9guliers", "criteria": {"min_visits": 3}, "created_at": "2025-05-17T20:27:22.290953"}, "converted_users": {"id": "converted_users", "name": "Utilisateurs ayant d\u00e9j\u00e0 achet\u00e9", "criteria": {"has_conversions": true}, "created_at": "2025-05-17T20:27:22.291297"}},
    
    // Initialiser le module
    init: function() {
        // Récupérer ou générer l'ID visiteur
        this.visitorId = this.getVisitorId();
        
        // Charger le profil utilisateur
        this.loadUserProfile();
        
        // Mettre à jour les données de visite
        this.updateVisitData();
        
        // Appliquer la personnalisation
        this.applyPersonalization();
        
        // Configurer le suivi des actions
        this.setupTracking();
        
        console.log("Personalization initialized for visitor", this.visitorId);
    },
    
    // Obtenir l'ID du visiteur
    getVisitorId: function() {
        let id = localStorage.getItem('visitor_id');
        if (!id) {
            id = 'v_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
            localStorage.setItem('visitor_id', id);
        }
        return id;
    },
    
    // Charger le profil utilisateur
    loadUserProfile: function() {
        let profile = localStorage.getItem('user_profile');
        if (profile) {
            try {
                this.userProfile = JSON.parse(profile);
            } catch (e) {
                console.error("Error parsing user profile:", e);
                this.userProfile = this.createDefaultProfile();
            }
        } else {
            this.userProfile = this.createDefaultProfile();
        }
    },
    
    // Créer un profil par défaut
    createDefaultProfile: function() {
        return {
            visits: 0,
            interests: [],
            last_products_viewed: [],
            conversions: [],
            device_type: this.detectDeviceType(),
            location: 'unknown',
            created_at: new Date().toISOString()
        };
    },
    
    // Détecter le type d'appareil
    detectDeviceType: function() {
        const userAgent = navigator.userAgent.toLowerCase();
        if (/android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent)) {
            return 'mobile';
        } else if (/tablet|ipad/i.test(userAgent)) {
            return 'tablet';
        } else {
            return 'desktop';
        }
    },
    
    // Mettre à jour les données de visite
    updateVisitData: function() {
        this.userProfile.visits += 1;
        this.userProfile.last_visit = new Date().toISOString();
          // Détecter les intérêts basés sur l'URL actuelle
        const currentPath = window.location.pathname;
          if (currentPath.includes('/posts/')) {            // Extraire la catégorie de l'article
            const categoryMatch = currentPath.match(/\/category\/([^/]+)/);
            if (categoryMatch && categoryMatch[1]) {
                const category = categoryMatch[1].replace(/-/g, ' ');
                if (!this.userProfile.interests.includes(category)) {
                    this.userProfile.interests.push(category);
                }
            }
        }
        
        // Sauvegarder le profil mis à jour
        this.saveUserProfile();
        
        // Envoyer les données au serveur
        this.syncProfileWithServer();
    },
    
    // Sauvegarder le profil utilisateur
    saveUserProfile: function() {
        localStorage.setItem('user_profile', JSON.stringify(this.userProfile));
    },
    
    // Synchroniser le profil avec le serveur
    syncProfileWithServer: function() {
        // Dans une implémentation réelle, envoyer le profil au serveur
        // Pour cette version, nous allons juste simuler
        console.log("Syncing profile with server:", this.userProfile);
    },
    
    // Vérifier si l'utilisateur est dans un segment
    isUserInSegment: function(segmentId) {
        if (!this.segments[segmentId]) return false;
        
        const segment = this.segments[segmentId];
        const criteria = segment.criteria;
        
        // Vérifier chaque critère
        for (const key in criteria) {
            const value = criteria[key];
            
            if (key === 'min_visits') {
                if (this.userProfile.visits < value) return false;
            }
            else if (key === 'interests') {
                // L'utilisateur doit avoir au moins un des intérêts listés
                if (!value.some(interest => this.userProfile.interests.includes(interest))) return false;
            }
            else if (key === 'viewed_products') {
                // L'utilisateur doit avoir vu au moins un des produits listés
                if (!value.some(product => this.userProfile.last_products_viewed.includes(product))) return false;
            }
            else if (key === 'has_conversions') {
                // L'utilisateur doit avoir au moins une conversion
                if (value && this.userProfile.conversions.length === 0) return false;
            }
            else if (key === 'device_type') {
                // L'utilisateur doit utiliser un certain type d'appareil
                if (this.userProfile.device_type !== value) return false;
            }
            else if (key === 'location') {
                // L'utilisateur doit être dans une certaine région
                if (this.userProfile.location !== value) return false;
            }
        }
        
        return true;
    },
    
    // Appliquer la personnalisation à la page
    applyPersonalization: function() {
        const currentPath = window.location.pathname;
        
        // Identifier la page
        let pageId = 'default';
        if (currentPath === '/' || currentPath === '/index.html') {
            pageId = 'home';
        } else if (currentPath.includes('/posts/')) {
            pageId = 'article';
        } else if (currentPath.includes('/category/')) {
            pageId = 'category';
        }
        
        // Parcourir les règles pour cette page
        if (this.rules[pageId]) {
            const pageRules = this.rules[pageId];
            
            for (const ruleId in pageRules) {
                const rule = pageRules[ruleId];
                const segmentId = rule.segment_id;
                
                // Vérifier si l'utilisateur est dans le segment
                if (this.isUserInSegment(segmentId)) {
                    this.applyRule(rule);
                }
            }
        }
    },
    
    // Appliquer une règle de personnalisation
    applyRule: function(rule) {
        const contentType = rule.content_type;
        const content = rule.content;
        
        if (contentType === 'header') {
            document.querySelector('.post-title').textContent = content;
        }
        else if (contentType === 'cta_text') {
            document.querySelectorAll('.cta-button').forEach(btn => {
                btn.textContent = content;
            });
        }
        else if (contentType === 'cta_style') {
            const style = document.createElement('style');
            style.textContent = '.cta-button { ' + content + ' }';
            document.head.appendChild(style);
        }
        else if (contentType === 'recommended_products') {
            // Insérer les produits recommandés
            const container = document.querySelector('.recommendations');
            if (container) {
                let html = '<h3>Recommandations personnalisées</h3><div class="product-grid">';
                
                content.forEach(product => {
                    html += `
                    <div class="product-card">
                        <h4>${product.name}</h4>
                        <div class="price">${product.price}</div>
                        <a href="/go/${product.slug}.html" class="cta-button">Voir l'offre</a>
                    </div>
                    `;
                });
                
                html += '</div>';
                container.innerHTML = html;
            }
        }
    },
    
    // Configurer le suivi des actions
    setupTracking: function() {        // Suivre les clics sur les liens d'affiliation
        document.querySelectorAll('a[href^="/go/"]').forEach(link => {
            link.addEventListener('click', e => {                const productSlug = link.href.match(/\/go\/([^.]+)\.html/)[1];
                
                // Ajouter le produit aux produits vus
                if (!this.userProfile.last_products_viewed.includes(productSlug)) {
                    this.userProfile.last_products_viewed.unshift(productSlug);
                    this.userProfile.last_products_viewed = this.userProfile.last_products_viewed.slice(0, 10);
                }
                
                // Sauvegarder le profil
                this.saveUserProfile();
            });
        });
    },
    
    // Enregistrer une conversion
    trackConversion: function(productSlug) {
        this.userProfile.conversions.push({
            product: productSlug,
            timestamp: new Date().toISOString()
        });
        
        this.saveUserProfile();
        this.syncProfileWithServer();
    },
    
    // Définir un intérêt utilisateur    setInterest: function(interest) {
        if (!this.userProfile.interests.includes(interest)) {
            this.userProfile.interests.push(interest);
            this.saveUserProfile();
            this.syncProfileWithServer();
        }
    }
};

// Initialiser au chargement
document.addEventListener('DOMContentLoaded', function() {
    Personalization.init();
});
