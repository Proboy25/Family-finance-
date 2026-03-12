# Guide d'Optimisation et Implémentation Wix pour VivaTerra Cameroun

Ce document contient les recommandations pour optimiser le site web www.vivaterracameroun.com, ajuster les pourcentages de réduction de votre pop-up (Lightbox) et intégrer le code de calcul automatique pour votre formulaire de devis.

## 1. Ajustement des "Flags" (Pop-up promotionnelle)

Voici les calculs exacts des réductions à afficher sur votre Pop-up pour les commandes de plus de 10 000 briques :

* **Briques perforées stabilisées :** De 230 à 160 FCFA -> **-30% de réduction** (exactement 30.4%)
* **Briques pleines stabilisées :** De 250 à 180 FCFA -> **-28% de réduction**
* **Briques de chaînage en U :** De 300 à 200 FCFA -> **-33% de réduction**
* **Briques perforées stabilisées sans ciment :** De 125 à 107 FCFA -> **-14% de réduction** (exactement 14.4%)
* **Briques pleines stabilisées sans ciment :** De 150 à 115 FCFA -> **-23% de réduction** (exactement 23.3%)

**Conseil pour la Pop-up :**
Pour plus d'impact marketing, vous pouvez regrouper le message :
> **"JUSQU'À -33% DE RÉDUCTION POUR LES COMMANDES DE PLUS DE 10 000 BRIQUES !"**
> *(Exemple : Briques de chaînage en U à 200 FCFA au lieu de 300 FCFA)*

---

## 2. Implémentation du Code Velo (Calculateur de Devis)

Pour automatiser le calcul des prix réduits dans votre formulaire de devis sur Wix, vous devez activer le "Mode Dev" (Velo) dans l'éditeur Wix et ajouter le code suivant sur la page de votre formulaire.

**Prérequis :**
Assurez-vous que les éléments de votre formulaire ont les ID (Identifiants) correspondants :
* Liste déroulante des types de briques : `#dropdownTypeBrique`
* Champ de saisie de la quantité : `#inputQuantite`
* Texte affichant le prix total : `#textPrixTotal`

**Code à copier-coller dans l'éditeur Velo :**

```javascript
// Fonction exécutée au chargement de la page
$w.onReady(function () {
    // Écoute les changements sur le type de brique et la quantité
    $w('#dropdownTypeBrique').onChange(calculerDevis);
    $w('#inputQuantite').onChange(calculerDevis);
});

// Fonction de calcul du devis
function calculerDevis() {
    const typeBrique = $w('#dropdownTypeBrique').value;
    const quantite = Number($w('#inputQuantite').value);

    let prixUnitaire = 0;

    // Vérification de la condition "Plus de 10 000 briques"
    if (quantite > 10000) {
        // Prix réduits (Tarifs de gros)
        switch(typeBrique) {
            case 'perforees_stabilisees': prixUnitaire = 160; break;
            case 'pleines_stabilisees': prixUnitaire = 180; break;
            case 'chainage_u': prixUnitaire = 200; break;
            case 'perforees_sans_ciment': prixUnitaire = 107; break;
            case 'pleines_sans_ciment': prixUnitaire = 115; break;
            default: prixUnitaire = 0;
        }
    } else {
        // Prix normaux
        switch(typeBrique) {
            case 'perforees_stabilisees': prixUnitaire = 230; break;
            case 'pleines_stabilisees': prixUnitaire = 250; break;
            case 'chainage_u': prixUnitaire = 300; break;
            case 'perforees_sans_ciment': prixUnitaire = 125; break;
            case 'pleines_sans_ciment': prixUnitaire = 150; break;
            default: prixUnitaire = 0;
        }
    }

    // Calcul et affichage du total
    const total = prixUnitaire * quantite;

    if (total > 0) {
        // Formate le nombre avec des espaces (ex: 1 500 000)
        $w('#textPrixTotal').text = total.toLocaleString('fr-FR') + " FCFA";
    } else {
        $w('#textPrixTotal').text = "0 FCFA";
    }
}
```

---

## 3. Bonnes Pratiques d'Optimisation SEO et Conversion

### A. Optimisation de la Conversion (Ventes)
1. **Appel à l'action (Call to Action - CTA) clair :** Les boutons de demande de devis doivent être très visibles (couleurs contrastées comme le orange ou le vert) avec des textes d'action comme "Demander un Devis Gratuit" ou "Profiter de l'Offre de Gros".
2. **Preuve Sociale :** Ajoutez des témoignages de clients ou des photos de chantiers réels ayant utilisé vos briques. Cela rassure les acheteurs potentiels de gros volumes.
3. **Optimisation de la Pop-up (Lightbox) :** Ne la faites pas apparaître *immédiatement*. Configurez un délai de 5 à 10 secondes ou un déclenchement lorsque le visiteur fait défiler 30% de la page. Une apparition immédiate peut faire fuir les visiteurs.

### B. Optimisation SEO (Visibilité sur Google)
1. **Balises Title et Meta Description :** Assurez-vous que chaque page (Accueil, Catalogue, Contact) possède des balises SEO personnalisées dans Wix. Utilisez des mots-clés comme "Briques stabilisées Cameroun", "Achat briques de construction Yaoundé/Douala", "Matériaux écologiques".
2. **Textes Alternatifs des Images (Alt Text) :** Wix permet d'ajouter un texte descriptif à chaque image. Décrivez les briques en utilisant vos mots-clés ("Brique pleine stabilisée pour construction au Cameroun").
3. **Vitesse de chargement :** Compressez vos images avant de les télécharger sur Wix (utilisez le format WebP ou JPEG optimisé). Trop d'images lourdes ralentissent le site, ce qui pénalise le SEO et fait fuir les clients sur mobile.
4. **Mobile-First :** Dans l'éditeur Wix, basculez sur la vue Mobile et ajustez les éléments pour que l'expérience sur smartphone soit parfaite (beaucoup de clients navigueront depuis leur téléphone).
