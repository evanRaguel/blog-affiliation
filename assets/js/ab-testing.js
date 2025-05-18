
// AB Testing Module
const ABTesting = {    // Tests actifs
    activeTests: {"cta_text_test": {"id": "cta_text_test", "name": "Test de texte du bouton CTA", "type": "content", "variants": {"variant_a": {".cta-button": "VOIR LES PRIX"}, "variant_b": {".cta-button": "VOIR L'OFFRE EXCLUSIVE"}, "variant_c": {".cta-button": "\u00c9CONOMISEZ 20% MAINTENANT"}}, "start_date": "2025-05-17T16:54:27.000860", "is_active": true, "impressions": {"variant_a": 0, "variant_b": 0, "variant_c": 0}, "conversions": {"variant_a": 0, "variant_b": 0, "variant_c": 0}, "target_pages": []}, "cta_color_test": {"id": "cta_color_test", "name": "Test de couleur du bouton CTA", "type": "style", "variants": {"variant_a": {".cta-button": {"background-color": "#f59e0b", "color": "#ffffff"}}, "variant_b": {".cta-button": {"background-color": "#dc2626", "color": "#ffffff"}}, "variant_c": {".cta-button": {"background-color": "#059669", "color": "#ffffff"}}}, "start_date": "2025-05-17T16:54:27.001523", "is_active": true, "impressions": {"variant_a": 0, "variant_b": 0, "variant_c": 0}, "conversions": {"variant_a": 0, "variant_b": 0, "variant_c": 0}, "target_pages": []}, "email_form_position": {"id": "email_form_position", "name": "Test de position du formulaire d'inscription", "type": "layout", "variants": {"variant_a": {".email-capture": {"action": "after", "reference": ".post-header"}}, "variant_b": {".email-capture": {"action": "before", "reference": ".conclusion-cta"}}}, "start_date": "2025-05-17T16:54:27.002034", "is_active": true, "impressions": {"variant_a": 0, "variant_b": 0}, "conversions": {"variant_a": 0, "variant_b": 0}, "target_pages": []}},
    
    // Identifiant visiteur
    visitorId: null,
    
    // Initialiser les tests
    init: function() {
        // Générer ou récupérer l'ID visiteur
        this.visitorId = this.getVisitorId();
        console.log("AB Testing initialized for visitor", this.visitorId);
        
        // Appliquer les tests à la page actuelle
        this.applyTests();
    },
    
    // Obtenir l'ID du visiteur depuis le stockage local ou en créer un
    getVisitorId: function() {
        let id = localStorage.getItem('ab_visitor_id');
        if (!id) {
            id = 'v_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
            localStorage.setItem('ab_visitor_id', id);
        }
        return id;
    },
    
    // Appliquer les tests à la page actuelle
    applyTests: function() {
        const currentPath = window.location.pathname;
        
        // Parcourir tous les tests actifs
        for (const testId in this.activeTests) {
            const test = this.activeTests[testId];
            
            // Vérifier si ce test s'applique à cette page
            if (test.target_pages.length === 0 || test.target_pages.some(pattern => new RegExp(pattern).test(currentPath))) {
                // Obtenir la variante pour ce visiteur
                const variantKey = this.getVariantForVisitor(testId);
                
                // Récupérer les données de la variante
                const variantData = test.variants[variantKey];
                
                // Appliquer la variante à la page
                this.applyVariant(test.type, variantData);
                
                // Stocker la variante vue par ce visiteur
                this.storeVariantImpression(testId, variantKey);
            }
        }
        
        // Ajouter des gestionnaires d'événements pour les conversions
        this.setupConversionTracking();
    },
    
    // Obtenir la variante pour un visiteur spécifique
    getVariantForVisitor: function(testId) {
        const test = this.activeTests[testId];
        const variantKeys = Object.keys(test.variants);
        
        // Hachage déterministe basé sur l'ID visiteur et l'ID du test
        const str = this.visitorId + ":" + testId;
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash = hash & hash; // Convertir en entier 32 bits
        }
        
        // Utiliser le hachage pour sélectionner la variante
        const index = Math.abs(hash) % variantKeys.length;
        return variantKeys[index];
    },
    
    // Appliquer une variante à la page
    applyVariant: function(testType, variantData) {
        switch (testType) {
            case 'content':
                // Remplacer du contenu
                for (const selector in variantData) {
                    const elements = document.querySelectorAll(selector);
                    elements.forEach(el => {
                        if (typeof variantData[selector] === 'string') {
                            el.innerHTML = variantData[selector];
                        } else if (typeof variantData[selector] === 'object') {
                            // Appliquer des attributs
                            for (const attr in variantData[selector]) {
                                el.setAttribute(attr, variantData[selector][attr]);
                            }
                        }
                    });
                }
                break;
                
            case 'style':
                // Appliquer des styles
                let styleEl = document.createElement('style');
                let cssText = '';
                for (const selector in variantData) {
                    cssText += selector + ' { ';
                    for (const prop in variantData[selector]) {
                        cssText += prop + ': ' + variantData[selector][prop] + '; ';
                    }
                    cssText += '} ';
                }
                styleEl.textContent = cssText;
                document.head.appendChild(styleEl);
                break;
                
            case 'layout':
                // Modifier la disposition des éléments
                for (const selector in variantData) {
                    const targetEl = document.querySelector(selector);
                    if (targetEl) {
                        const action = variantData[selector].action;
                        const referenceSelector = variantData[selector].reference;
                        const referenceEl = document.querySelector(referenceSelector);
                        
                        if (referenceEl && action) {
                            if (action === 'before') {
                                referenceEl.parentNode.insertBefore(targetEl, referenceEl);
                            } else if (action === 'after') {
                                referenceEl.parentNode.insertBefore(targetEl, referenceEl.nextSibling);
                            } else if (action === 'prepend') {
                                referenceEl.prepend(targetEl);
                            } else if (action === 'append') {
                                referenceEl.append(targetEl);
                            }
                        }
                    }
                }
                break;
        }
    },
    
    // Stocker l'impression d'une variante
    storeVariantImpression: function(testId, variantKey) {
        // Stocker localement quelle variante a été vue
        const key = 'ab_test_' + testId;
        localStorage.setItem(key, variantKey);
        
        // Envoyer l'impression au serveur
        this.sendAnalyticsEvent('impression', testId, variantKey);
    },
    
    // Configurer le suivi des conversions
    setupConversionTracking: function() {
        // Suivre les clics sur les liens d'affiliation
        document.querySelectorAll('a[href^="/go/"]').forEach(link => {
            link.addEventListener('click', e => {
                // Pour chaque test actif, vérifier si le visiteur a vu une variante
                for (const testId in this.activeTests) {
                    const variantKey = localStorage.getItem('ab_test_' + testId);
                    if (variantKey) {
                        this.trackConversion(testId, variantKey);
                    }
                }
            });
        });
        
        // Suivre les soumissions de formulaire
        document.querySelectorAll('form.email-form').forEach(form => {
            form.addEventListener('submit', e => {
                // Pour chaque test actif, vérifier si le visiteur a vu une variante
                for (const testId in this.activeTests) {
                    const variantKey = localStorage.getItem('ab_test_' + testId);
                    if (variantKey) {
                        this.trackConversion(testId, variantKey, 'email_signup');
                    }
                }
            });
        });
    },
    
    // Suivre une conversion
    trackConversion: function(testId, variantKey, conversionType = 'click') {
        // Envoyer la conversion au serveur
        this.sendAnalyticsEvent('conversion', testId, variantKey, conversionType);
        return true;
    },
    
    // Envoyer un événement d'analyse au serveur
    sendAnalyticsEvent: function(eventType, testId, variantKey, conversionType = null) {
        const data = {
            event: eventType,
            testId: testId,
            variantKey: variantKey,
            visitorId: this.visitorId,
            timestamp: new Date().toISOString(),
            page: window.location.pathname
        };
        
        if (conversionType) {
            data.conversionType = conversionType;
        }
        
        // Envoyer à l'API d'analytics du site
        const endpoint = '/api/ab-event';
        
        // Pour cette version, nous allons simplement journaliser l'événement
        // Une implémentation réelle enverrait les données au serveur
        console.log('AB Testing Event:', data);
        
        // Stocker localement pour démonstration
        try {
            const abEvents = JSON.parse(localStorage.getItem('ab_events') || '[]');
            abEvents.push(data);
            localStorage.setItem('ab_events', JSON.stringify(abEvents));
        } catch (e) {
            console.error('Error storing AB event:', e);
        }
    }
};

// Initialiser au chargement
document.addEventListener('DOMContentLoaded', function() {
    ABTesting.init();
});
