function toggleVisibility() {
  const input = document.getElementById('passwordInput');
  const btn = document.querySelector('.toggle-btn');
  if (input.type === 'password') {
    input.type = 'text';
    btn.textContent = 'Masquer';
  } else {
    input.type = 'password';
    btn.textContent = 'Voir';
  }
}

/* ---------- Estimation du temps de cassage ---------- */
/* Hypothèse : mot de passe tiré au hasard, 10 milliards d'essais par seconde. */
function estimateCrackTime(password) {
  let charset = 0;
  if (/[a-z]/.test(password)) charset += 26;
  if (/[A-Z]/.test(password)) charset += 26;
  if (/[0-9]/.test(password)) charset += 10;
  if (/[^a-zA-Z0-9]/.test(password)) charset += 32;

  const combinations = Math.pow(charset, password.length);
  const guessesPerSecond = 1e10;
  const seconds = combinations / guessesPerSecond;

  if (seconds < 1) return { time: "moins d'une seconde", level: "red" };
  if (seconds < 60) return { time: Math.round(seconds) + " secondes", level: "red" };
  if (seconds < 3600) return { time: Math.round(seconds / 60) + " minutes", level: "red" };
  if (seconds < 86400) return { time: Math.round(seconds / 3600) + " heures", level: "orange" };
  if (seconds < 2592000) return { time: Math.round(seconds / 86400) + " jours", level: "orange" };
  if (seconds < 31536000) return { time: Math.round(seconds / 2592000) + " mois", level: "orange" };
  if (seconds < 3153600000) return { time: Math.round(seconds / 31536000) + " ans", level: "green" };
  return { time: "plus de 100 ans", level: "green" };
}

/* ---------- Analyse des habitudes ---------- */
const commonPasswords = ['password', 'motdepasse', '123456', 'azerty', 'qwerty', 'admin', 'bonjour', 'soleil', 'football', 'iloveyou'];

// Remplace les substitutions courantes (@ -> a, 3 -> e, 0 -> o...) pour retrouver le mot d'origine
const leetMap = { '@': 'a', '4': 'a', '3': 'e', '1': 'i', '!': 'i', '0': 'o', '$': 's', '5': 's' };
function normalise(text) {
  return text.toLowerCase().replace(/[@431!05$]/g, c => leetMap[c]);
}

function analyzeHabits(password) {
  const issues = [];
  const lower = password.toLowerCase();
  const deLeeted = normalise(password);

  if (commonPasswords.some(p => lower.includes(p))) {
    issues.push("Contient un mot de passe très courant, facile à deviner");
  } else if (commonPasswords.some(p => deLeeted.includes(p))) {
    issues.push("Utilise des substitutions connues (@ pour a, 3 pour e, 0 pour o...) sur un mot courant : les outils de cassage les connaissent");
  }

  // Un même caractère répété 3 fois d'affilée ou plus (aaa, 111)
  if (/(.)\1{2,}/.test(password)) {
    issues.push("Contient un caractère répété plusieurs fois d'affilée (ex : aaa, 111)");
  }

  if (/^[a-zA-Z]+\d{2,4}$/.test(password)) {
    issues.push("Suit le schéma classique mot + chiffres (ex : marie1990)");
  }

  if (password.length < 12) {
    issues.push("Court : 12 caractères minimum sont recommandés");
  }

  return issues;
}

/* ---------- Vérification dans les fuites (Have I Been Pwned, k-anonymat) ---------- */
/* Retourne le nombre de fois où le mot de passe apparaît dans des fuites,
   0 s'il n'est pas trouvé, -1 si la vérification est impossible. */
async function checkHIBP(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-1', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();

  // Seuls les 5 premiers caractères de l'empreinte sont envoyés
  const prefix = hashHex.substring(0, 5);
  const suffix = hashHex.substring(5);

  try {
    const response = await fetch('https://api.pwnedpasswords.com/range/' + prefix);
    if (!response.ok) return -1; // erreur du service : on ne dit pas "non trouvé"
    const text = await response.text();

    for (const line of text.split('\n')) {
      const [hashSuffix, count] = line.trim().split(':');
      if (hashSuffix === suffix) {
        return parseInt(count, 10) || 0;
      }
    }
    return 0;
  } catch (e) {
    return -1;
  }
}

/* ---------- Générateur (méthode des mots) ---------- */
const words = [
  'cheval', 'lampe', 'nuage', 'carotte', 'bureau', 'fenetre', 'montagne', 'riviere', 'ballon', 'miroir',
  'bougie', 'jardin', 'papier', 'musique', 'voyage', 'silence', 'lumiere', 'foret', 'saison', 'orange',
  'citron', 'pomme', 'poire', 'cerise', 'fraise', 'tomate', 'salade', 'fromage', 'gateau', 'chocolat',
  'biscuit', 'bonbon', 'cuisine', 'assiette', 'fourchette', 'couteau', 'bouteille', 'verre', 'tasse', 'theiere',
  'armoire', 'tableau', 'chaise', 'canape', 'tapis', 'rideau', 'oreiller', 'couverture', 'escalier', 'balcon',
  'terrasse', 'grenier', 'cave', 'garage', 'portail', 'barriere', 'chemin', 'sentier', 'village', 'ville',
  'plage', 'ocean', 'vague', 'sable', 'rocher', 'falaise', 'ile', 'phare', 'bateau', 'voilier',
  'avion', 'train', 'camion', 'velo', 'moto', 'tracteur', 'fusee', 'tramway', 'metro', 'bus',
  'etoile', 'planete', 'comete', 'galaxie', 'orage', 'eclair', 'tonnerre', 'arcenciel', 'brouillard', 'neige',
  'pluie', 'vent', 'glace', 'givre', 'rosee', 'brume', 'nuit', 'matin', 'aube', 'crepuscule',
  'renard', 'loup', 'ours', 'lapin', 'souris', 'chat', 'chien', 'oiseau', 'hibou', 'aigle',
  'dauphin', 'baleine', 'requin', 'poisson', 'crabe', 'tortue', 'grenouille', 'papillon', 'abeille', 'fourmi',
  'chene', 'sapin', 'bouleau', 'saule', 'olivier', 'rosier', 'lavande', 'tulipe', 'muguet', 'pissenlit',
  'violon', 'piano', 'guitare', 'flute', 'tambour', 'trompette', 'harpe', 'accordeon', 'cloche', 'orgue',
  'crayon', 'stylo', 'cahier', 'livre', 'carte', 'regle', 'gomme', 'pinceau', 'toile', 'palette',
  'marteau', 'tournevis', 'clou', 'scie', 'pince', 'echelle', 'seau', 'brosse', 'balai', 'eponge',
  'horloge', 'montre', 'boussole', 'jumelles', 'lunettes', 'parapluie', 'valise', 'sac', 'chapeau', 'echarpe',
  'manteau', 'botte', 'gant', 'ceinture', 'bouton', 'fil', 'aiguille', 'ciseau', 'ruban', 'dentelle',
  'tigre', 'lion', 'zebre', 'girafe', 'panda', 'koala', 'kangourou', 'lama', 'chameau', 'elephant',
  'safran', 'cannelle', 'vanille', 'menthe', 'basilic', 'thym', 'romarin', 'persil', 'poivre', 'sel'
];

const NB_MOTS = 6;

// Tirage aléatoire sécurisé (crypto.getRandomValues), sans biais
function randInt(max) {
  const buffer = new Uint32Array(1);
  const limit = Math.floor(0x100000000 / max) * max;
  do {
    crypto.getRandomValues(buffer);
  } while (buffer[0] >= limit);
  return buffer[0] % max;
}

function generatePassword() {
  const selected = [];
  for (let i = 0; i < NB_MOTS; i++) {
    selected.push(words[randInt(words.length)]);
  }
  document.getElementById('generated-pwd').textContent = selected.join('-');
}

function copyPassword() {
  const pwd = document.getElementById('generated-pwd').textContent;
  if (pwd === 'Cliquez sur Générer') return;
  navigator.clipboard.writeText(pwd).then(
    () => alert('Mot de passe copié !'),
    () => alert('Copie impossible : sélectionnez le texte et copiez-le à la main.')
  );
}

/* ---------- Analyse complète ---------- */
async function analyzePassword() {
  const password = document.getElementById('passwordInput').value;
  if (!password) return;

  document.getElementById('results').style.display = 'block';

  const crack = estimateCrackTime(password);
  const crackCard = document.getElementById('crack-card');
  crackCard.className = 'card ' + crack.level;
  document.getElementById('crack-time').textContent = crack.time;

  const crackDescs = {
    red: "Un ordinateur équipé d'une bonne carte graphique peut essayer des milliards de combinaisons par seconde. Ce mot de passe ne résisterait pas longtemps.",
    orange: "Pas suffisant. Un attaquant motivé avec du matériel dédié pourrait casser ce mot de passe.",
    green: "Bonne résistance face à une attaque par force brute."
  };
  const hypothese = " Estimation pour un mot de passe tiré au hasard, à 10 milliards d'essais par seconde : un mot de passe construit à partir de mots courants se casse beaucoup plus vite.";
  document.getElementById('crack-desc').textContent = crackDescs[crack.level] + hypothese;

  document.getElementById('hibp-value').textContent = 'Vérification en cours...';
  const hibpCount = await checkHIBP(password);
  const hibpCard = document.getElementById('hibp-card');

  if (hibpCount === -1) {
    hibpCard.className = 'card blue';
    document.getElementById('hibp-value').textContent = 'Vérification impossible';
    document.getElementById('hibp-desc').textContent = 'Impossible de contacter le service de vérification. Votre connexion est peut-être limitée.';
  } else if (hibpCount === 0) {
    hibpCard.className = 'card green';
    document.getElementById('hibp-value').textContent = 'Non trouvé dans les fuites';
    document.getElementById('hibp-desc').textContent = "Ce mot de passe n'apparaît pas dans les bases de mots de passe volés connues. Attention : cela ne signifie pas qu'il est fort.";
  } else {
    hibpCard.className = 'card red';
    document.getElementById('hibp-value').textContent = hibpCount.toLocaleString('fr-FR') + ' fois volé';
    document.getElementById('hibp-desc').textContent = "Ce mot de passe exact a été trouvé " + hibpCount.toLocaleString('fr-FR') + " fois dans des fuites de données. N'importe quel attaquant peut l'essayer en priorité sur vos comptes.";
  }

  const issues = analyzeHabits(password);
  const habitsCard = document.getElementById('habits-card');

  if (issues.length === 0) {
    habitsCard.className = 'card green';
    document.getElementById('habits-value').textContent = 'Aucun problème détecté';
    document.getElementById('habits-desc').textContent = "Ce mot de passe ne présente pas de schéma facilement prévisible parmi ceux que cet outil sait repérer.";
  } else {
    habitsCard.className = 'card ' + (issues.length >= 2 ? 'red' : 'orange');
    document.getElementById('habits-value').textContent = issues.length + ' problème(s) détecté(s)';
    document.getElementById('habits-desc').textContent = issues.join('. ') + '.';
  }
}

document.getElementById('passwordInput').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') analyzePassword();
});
