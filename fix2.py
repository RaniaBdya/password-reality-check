js = '''function toggleVisibility() {
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

function estimateCrackTime(password) {
  let charset = 0;
  if (/[a-z]/.test(password)) charset += 26;
  if (/[A-Z]/.test(password)) charset += 26;
  if (/[0-9]/.test(password)) charset += 10;
  if (/[^a-zA-Z0-9]/.test(password)) charset += 32;

  const combinations = Math.pow(charset, password.length);
  const guessesPerSecond = 1e10;
  const seconds = combinations / guessesPerSecond;

  if (seconds < 1) return { time: "moins d\'une seconde", level: "red" };
  if (seconds < 60) return { time: Math.round(seconds) + " secondes", level: "red" };
  if (seconds < 3600) return { time: Math.round(seconds/60) + " minutes", level: "red" };
  if (seconds < 86400) return { time: Math.round(seconds/3600) + " heures", level: "orange" };
  if (seconds < 2592000) return { time: Math.round(seconds/86400) + " jours", level: "orange" };
  if (seconds < 31536000) return { time: Math.round(seconds/2592000) + " mois", level: "orange" };
  if (seconds < 3153600000) return { time: Math.round(seconds/31536000) + " ans", level: "green" };
  return { time: "plus de 100 ans", level: "green" };
}

function analyzeHabits(password) {
  const issues = [];

  const commonPasswords = ['password', 'motdepasse', '123456', 'azerty', 'qwerty', 'admin', 'bonjour', 'soleil', 'football', 'iloveyou'];
  if (commonPasswords.some(p => password.toLowerCase().includes(p))) {
    issues.push("Contient un mot de passe très courant facilement deviné");
  }

  if (/(.)\1{2,}/.test(password)) {
    issues.push("Contient des caractères répétés (ex: aaa, 111)");
  }

  if (/^[a-zA-Z]+\d{2,4}$/.test(password)) {
    issues.push("Suit le schéma classique mot + année (ex: marie1990)");
  }

  if (/[a@][a@]|[e3][e3]|[i1!][i1!]|[o0][o0]/.test(password.toLowerCase())) {
    issues.push("Utilise des substitutions connues (@=a, 3=e, 0=o) : les outils de cassage les connaissent toutes");
  }

  if (password.length < 8) {
    issues.push("Trop court : minimum 12 caractères recommandés");
  }

  return issues;
}

async function checkHIBP(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-1', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();

  const prefix = hashHex.substring(0, 5);
  const suffix = hashHex.substring(5);

  try {
    const response = await fetch('https://api.pwnedpasswords.com/range/' + prefix);
    const text = await response.text();
    const lines = text.split('\\n');

    for (const line of lines) {
      const [hashSuffix, count] = line.split(':');
      if (hashSuffix.trim() === suffix) {
        return parseInt(count.trim());
      }
    }
    return 0;
  } catch (e) {
    return -1;
  }
}

const words = ['cheval', 'lampe', 'nuage', 'carotte', 'bureau', 'fenetre', 'montagne', 'riviere', 'ballon', 'miroir', 'soleil', 'bougie', 'jardin', 'papier', 'musique', 'voyage', 'silence', 'lumiere', 'foret', 'saison'];

function generatePassword() {
  const selected = [];
  const used = new Set();
  while (selected.length < 4) {
    const idx = Math.floor(Math.random() * words.length);
    if (!used.has(idx)) {
      used.add(idx);
      selected.push(words[idx]);
    }
  }
  const num = Math.floor(Math.random() * 90) + 10;
  document.getElementById('generated-pwd').textContent = selected.join('-') + '-' + num;
}

function copyPassword() {
  const pwd = document.getElementById('generated-pwd').textContent;
  navigator.clipboard.writeText(pwd);
  alert('Mot de passe copié !');
}

async function analyzePassword() {
  const password = document.getElementById('passwordInput').value;
  if (!password) return;

  document.getElementById('results').style.display = 'block';

  const crack = estimateCrackTime(password);
  const crackCard = document.getElementById('crack-card');
  crackCard.className = 'card ' + crack.level;
  document.getElementById('crack-time').textContent = crack.time;

  const crackDescs = {
    red: "Un ordinateur équipé d\'une bonne carte graphique peut essayer des milliards de combinaisons par seconde. Votre mot de passe ne résisterait pas longtemps.",
    orange: "Pas suffisant. Un attaquant motivé avec du matériel dédié pourrait casser ce mot de passe.",
    green: "Bonne résistance. Ce mot de passe résisterait aux attaques par force brute."
  };
  document.getElementById('crack-desc').textContent = crackDescs[crack.level];

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
    document.getElementById('hibp-desc').textContent = "Ce mot de passe n\'apparaît pas dans les bases de données de mots de passe volés connus. Attention : cela ne signifie pas qu\'il est fort.";
  } else {
    hibpCard.className = 'card red';
    document.getElementById('hibp-value').textContent = hibpCount.toLocaleString('fr-FR') + ' fois volé';
    document.getElementById('hibp-desc').textContent = "Ce mot de passe exact a été trouvé " + hibpCount.toLocaleString('fr-FR') + " fois dans des fuites de données. N\'importe quel attaquant peut l\'essayer en priorité sur vos comptes.";
  }

  const issues = analyzeHabits(password);
  const habitsCard = document.getElementById('habits-card');

  if (issues.length === 0) {
    habitsCard.className = 'card green';
    document.getElementById('habits-value').textContent = 'Aucun problème détecté';
    document.getElementById('habits-desc').textContent = "Ce mot de passe ne présente pas de schéma facilement prévisible.";
  } else {
    habitsCard.className = 'card ' + (issues.length >= 2 ? 'red' : 'orange');
    document.getElementById('habits-value').textContent = issues.length + ' problème(s) détecté(s)';
    document.getElementById('habits-desc').textContent = issues.join('. ');
  }
}

document.getElementById('passwordInput').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') analyzePassword();
});
'''

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("script.js écrit avec succès !")