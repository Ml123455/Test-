// ═══════════════════════════════════════════
// GÉNÉRATEUR DE SITE EN DIRECT
// Sync bidirectionnelle formulaire ↔ aperçu
// Sauvegarde automatique localStorage
// ═══════════════════════════════════════════

(function() {
  'use strict';

  // ── IDs des champs du formulaire ──
  var FIELD_IDS = [
    'gen-name', 'gen-job', 'gen-city', 'gen-exp',
    'gen-headline', 'gen-desc',
    'gen-s1', 'gen-s2', 'gen-s3'
  ];

  var STORAGE_KEY = 'sitegen-data';

  // ── Lire un champ formulaire ──
  function getVal(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : '';
  }

  // ── Écrire dans un champ formulaire ──
  function setVal(id, value) {
    var el = document.getElementById(id);
    if (el) el.value = value;
  }

  // ── Lire le texte d'un élément preview ──
  function getText(id) {
    var el = document.getElementById(id);
    return el ? el.textContent.trim() : '';
  }

  // ── Écrire le texte dans un élément preview ──
  function setText(id, text) {
    var el = document.getElementById(id);
    if (el && el.textContent !== text) {
      el.textContent = text;
    }
  }

  // ═══════════════════════════════════════════
  // FORM → PREVIEW (mise à jour de l'aperçu)
  // ═══════════════════════════════════════════
  function updatePreview() {
    var name = getVal('gen-name') || 'Votre Nom';
    var job = getVal('gen-job') || 'votre métier';
    var city = getVal('gen-city') || 'votre ville';
    var exp = getVal('gen-exp') || '';
    var headline = getVal('gen-headline') || 'Votre phrase d\'accroche ici';
    var desc = getVal('gen-desc') || 'Décrivez ce que vous faites. Parlez de votre expérience et de ce qui rend votre travail unique.';
    var s1 = getVal('gen-s1') || 'Service 1';
    var s2 = getVal('gen-s2') || 'Service 2';
    var s3 = getVal('gen-s3') || 'Service 3';

    // Logo : dernier mot du nom
    var logoWords = name.split(' ').filter(function(w) { return w.length > 0; });
    var logoText = logoWords.length > 0 ? logoWords[logoWords.length - 1].toUpperCase() : 'MON SITE';
    setText('prev-logo', logoText);

    // Badge
    var badgeText = '⭐ ';
    if (job !== 'votre métier') {
      badgeText += job.charAt(0).toUpperCase() + job.slice(1);
    } else {
      badgeText += 'Votre métier';
    }
    if (city !== 'votre ville') {
      badgeText += ' — ' + city;
    }
    setText('prev-badge', badgeText);

    // Headline
    setText('prev-headline', headline);

    // Description (sans les années d'expérience — l'utilisateur les met dans son texte si voulu)
    setText('prev-desc', desc);

    // Services
    setText('prev-s1', s1);
    setText('prev-s2', s2);
    setText('prev-s3', s3);

    // Trust badge experience
    var expEl = document.getElementById('prev-trust-exp');
    if (expEl) {
      var expNum = parseInt(exp, 10);
      if (!isNaN(expNum) && expNum > 0) {
        expEl.textContent = '✅ ' + expNum + ' an' + (expNum > 1 ? 's' : '') + ' d\'expérience';
      } else {
        expEl.textContent = '✅ Artisan passionné';
      }
    }

    // Footer
    var footerEl = document.getElementById('prev-footer');
    if (footerEl) {
      var footerName = name !== 'Votre Nom' ? name : '';
      var footerJob = job !== 'votre métier' ? job : '';
      var footerCity = city !== 'votre ville' ? city : '';

      var nameDiv = footerEl.querySelector('.prev-footer-name');
      var infoDiv = footerEl.querySelector('.prev-footer-info');
      if (nameDiv) nameDiv.textContent = footerName || 'Votre Nom';
      if (infoDiv) {
        var parts = [];
        if (footerJob) parts.push('Artisan ' + footerJob);
        if (footerCity) parts.push('à ' + footerCity);
        infoDiv.textContent = parts.length > 0 ? parts.join(' — ') : 'Votre entreprise';
      }
    }

    // Sauvegarder
    saveToStorage();
  }

  // ═══════════════════════════════════════════
  // PREVIEW → FORM (sync inverse)
  // ═══════════════════════════════════════════
  function syncFromPreview(el) {
    var fieldId = el.getAttribute('data-gen-field');
    var mode = el.getAttribute('data-gen-mode');
    if (!fieldId) return;

    var text = el.textContent.trim();

    switch (mode) {
      case 'lastname':
        // Le logo affiche le dernier mot : retrouver le nom complet
        var currentName = getVal('gen-name');
        var parts = currentName.split(' ').filter(function(w) { return w.length > 0; });
        if (parts.length > 0) {
          parts[parts.length - 1] = text;
          setVal('gen-name', parts.join(' '));
        } else {
          setVal('gen-name', text);
        }
        break;

      case 'badge':
        // Format: "⭐ Métier — Ville" → extraire métier et ville
        var cleaned = text.replace(/^⭐\s*/, '').trim();
        var dashIdx = cleaned.lastIndexOf(' — ');
        if (dashIdx > 0) {
          setVal('gen-job', cleaned.substring(0, dashIdx).trim().toLowerCase());
          setVal('gen-city', cleaned.substring(dashIdx + 3).trim());
        } else {
          setVal('gen-job', cleaned.toLowerCase());
        }
        break;

      case 'footer':
        // Footer a deux divs enfants, pas d'édition directe du parent
        // On lit les deux enfants
        var nameDiv = el.querySelector('.prev-footer-name');
        var infoDiv = el.querySelector('.prev-footer-info');
        if (nameDiv) {
          setVal('gen-name', nameDiv.textContent.trim());
        }
        if (infoDiv) {
          var infoText = infoDiv.textContent.trim();
          // Format: "Artisan métier — à ville"
          var artisanIdx = infoText.indexOf('Artisan ');
          var aIdx = infoText.indexOf(' — à ');
          if (artisanIdx >= 0) {
            var jobPart = '';
            var cityPart = '';
            if (aIdx > artisanIdx) {
              jobPart = infoText.substring(artisanIdx + 8, aIdx).trim();
              cityPart = infoText.substring(aIdx + 5).trim();
            } else {
              jobPart = infoText.substring(artisanIdx + 8).trim();
            }
            setVal('gen-job', jobPart.toLowerCase());
            setVal('gen-city', cityPart);
          }
        }
        break;

      default:
        // Simple 1:1 mapping
        setVal(fieldId, text);
        break;
    }

    // Re-sync depuis le formulaire pour tout remettre en cohérence
    updatePreview();
  }

  // ═══════════════════════════════════════════
  // SAUVEGARDE LOCALSTORAGE
  // ═══════════════════════════════════════════
  function saveToStorage() {
    var data = {};
    FIELD_IDS.forEach(function(id) {
      data[id] = getVal(id);
    });
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch(e) {
      // localStorage plein ou désactivé — silencieux
    }
  }

  function loadFromStorage() {
    var raw = null;
    try {
      raw = localStorage.getItem(STORAGE_KEY);
    } catch(e) {
      return false;
    }
    if (!raw) return false;
    try {
      var data = JSON.parse(raw);
      var hasData = false;
      FIELD_IDS.forEach(function(id) {
        if (data[id]) {
          setVal(id, data[id]);
          hasData = true;
        }
      });
      return hasData;
    } catch(e) {
      return false;
    }
  }

  // ═══════════════════════════════════════════
  // DÉFAUTS (Jean Dubois)
  // ═══════════════════════════════════════════
  var DEFAULTS = {
    'gen-name': 'Jean Dubois',
    'gen-job': 'menuisier ébéniste',
    'gen-city': 'Chartres',
    'gen-exp': '15',
    'gen-headline': 'Des meubles qui traversent les générations',
    'gen-desc': 'Je crée des meubles sur mesure depuis 15 ans à Chartres. Chaque pièce est unique, fabriquée à la main avec des bois nobles et des finitions soignées.',
    'gen-s1': 'Meubles sur mesure',
    'gen-s2': 'Rénovation de meubles anciens',
    'gen-s3': 'Agencement intérieur'
  };

  function loadDefaults() {
    Object.keys(DEFAULTS).forEach(function(id) {
      setVal(id, DEFAULTS[id]);
    });
  }

  // ═══════════════════════════════════════════
  // INITIALISATION
  // ═══════════════════════════════════════════
  document.addEventListener('DOMContentLoaded', function() {
    // Essayer de charger depuis localStorage
    var restored = loadFromStorage();

    if (!restored) {
      // Pas de sauvegarde → charger l'exemple de Jean Dubois
      loadDefaults();
    }

    // Appliquer les valeurs à l'aperçu
    updatePreview();

    // ── Écouteurs : preview contenteditable → form ──
    var editables = document.querySelectorAll('[contenteditable="true"]');
    editables.forEach(function(el) {
      // Sur input (moderne) ou blur (fallback)
      el.addEventListener('input', function() {
        syncFromPreview(el);
      });
      el.addEventListener('blur', function() {
        syncFromPreview(el);
      });
    });

    // ── Scroll sync optionnel : quand l'utilisateur tape dans le form,
    //     scroller l'aperçu pour montrer la section correspondante ──
    var formInputs = document.querySelectorAll('.demo-form-body .form-input');
    formInputs.forEach(function(input) {
      input.addEventListener('focus', function() {
        // Petit délai pour ne pas être agressif
        var fieldId = input.id;
        var targetMap = {
          'gen-name': 'prev-logo',
          'gen-job': 'prev-badge',
          'gen-city': 'prev-badge',
          'gen-exp': 'prev-trust-exp',
          'gen-headline': 'prev-headline',
          'gen-desc': 'prev-desc',
          'gen-s1': 'prev-s1',
          'gen-s2': 'prev-s2',
          'gen-s3': 'prev-s3'
        };
        var targetId = targetMap[fieldId];
        if (targetId) {
          var target = document.getElementById(targetId);
          if (target) {
            setTimeout(function() {
              target.scrollIntoView({ behavior: 'smooth', block: 'center' });
              // Flash highlight
              target.style.transition = 'outline-color 0.15s';
              target.style.outline = '2px solid var(--accent)';
              target.style.outlineOffset = '6px';
              target.style.borderRadius = '4px';
              setTimeout(function() {
                target.style.outline = '';
                target.style.outlineOffset = '';
                target.style.borderRadius = '';
              }, 1500);
            }, 200);
          }
        }
      });
    });
  });

})();
