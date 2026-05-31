html = '''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Password Reality Check</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      background: #0f0f1a;
      color: #e0e0e0;
      min-height: 100vh;
      padding: 40px 20px;
    }
    .container { max-width: 680px; margin: 0 auto; }
    h1 { font-size: 28px; color: #ffffff; margin-bottom: 8px; }
    .subtitle { color: #888; font-size: 15px; margin-bottom: 40px; }
    .input-zone { background: #1a1a2e; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
    .input-wrapper { display: flex; gap: 10px; margin-bottom: 12px; }
    input[type="password"], input[type="text"] {
      flex: 1; background: #0f0f1a; border: 1px solid #333;
      border-radius: 8px; padding: 12px 16px; color: white; font-size: 16px; outline: none;
    }
    input:focus { border-color: #e94560; }
    button {
      background: #e94560; color: white; border: none;
      border-radius: 8px; padding: 12px 20px; cursor: pointer; font-size: 14px; font-weight: bold;
    }
    button:hover { background: #c73652; }
    .toggle-btn { background: #333; padding: 12px 16px; }
    .toggle-btn:hover { background: #444; }
    .privacy-note { font-size: 12px; color: #666; }
    .results { display: none; }
    .card { background: #1a1a2e; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px; border-left: 4px solid #333; }
    .card.green { border-left-color: #4caf50; }
    .card.orange { border-left-color: #ff9800; }
    .card.red { border-left-color: #f44336; }
    .card.blue { border-left-color: #2196f3; }
    .card-title { font-size: 13px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .card-value { font-size: 22px; font-weight: bold; color: white; margin-bottom: 6px; }
    .card-desc { font-size: 14px; color: #aaa; line-height: 1.6; }
    .rgpd-section { background: #1a1a2e; border-radius: 12px; padding: 24px; margin-bottom: 16px; border-left: 4px solid #9c27b0; }
    .rgpd-section h3 { color: #ce93d8; margin-bottom: 12px; font-size: 16px; }
    .rgpd-section p { font-size: 14px; color: #aaa; line-height: 1.7; margin-bottom: 10px; }
    .generator { background: #1a1a2e; border-radius: 12px; padding: 24px; margin-bottom: 16px; }
    .generator h3 { color: #4caf50; margin-bottom: 16px; }
    .generated-password { background: #0f0f1a; border-radius: 8px; padding: 14px 18px; font-family: monospace; font-size: 18px; color: #4caf50; margin-bottom: 12px; word-break: break-all; }
    .gen-btn { background: #2e7d32; margin-right: 10px; }
    .gen-btn:hover { background: #1b5e20; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Password Reality Check</h1>
    <p class="subtitle">Découvrez vraiment à quel point votre mot de passe est sécurisé, en toute confidentialité.</p>
    <div class="input-zone">
      <div class="input-wrapper">
        <input type="password" id="passwordInput" placeholder="Entrez votre mot de passe..." />
        <button class="toggle-btn" onclick="toggleVisibility()">Voir</button>
        <button onclick="analyzePassword()">Analyser</button>
      </div>
      <p class="privacy-note">Votre mot de passe ne quitte jamais votre navigateur. Aucune donnée n\'est envoyée ni stockée.</p>
    </div>
    <div class="results" id="results">
      <div class="card" id="crack-card">
        <div class="card-title">Temps de cassage estimé</div>
        <div class="card-value" id="crack-time">-</div>
        <div class="card-desc" id="crack-desc">-</div>
      </div>
      <div class="card" id="hibp-card">
        <div class="card-title">Présence dans des fuites de données</div>
        <div class="card-value" id="hibp-value">Vérification...</div>
        <div class="card-desc" id="hibp-desc">-</div>
      </div>
      <div class="card" id="habits-card">
        <div class="card-title">Analyse des habitudes</div>
        <div class="card-value" id="habits-value">-</div>
        <div class="card-desc" id="habits-desc">-</div>
      </div>
      <div class="rgpd-section">
        <h3>Pourquoi c\'est important : le lien avec le RGPD</h3>
        <p>Quand vous créez un compte sur un site, votre mot de passe est stocké sous forme de hash, une empreinte numérique irréversible. Un bon site utilise des algorithmes modernes comme bcrypt ou argon2. Un mauvais site utilise MD5, un algorithme obsolète qui peut être cassé en moins d\'une seconde.</p>
        <p>L\'article 32 du RGPD oblige les entreprises à protéger vos données par des "mesures techniques appropriées". Stocker des mots de passe en MD5 est une violation directe de cet article.</p>
        <p>Aujourd\'hui, des millions de mots de passe issus de fuites de données circulent sur internet. Si votre mot de passe est dans ces bases, un attaquant peut l\'essayer sur tous vos comptes en quelques minutes.</p>
      </div>
      <div class="generator">
        <h3>Un vrai mot de passe sécurisé</h3>
        <div class="generated-password" id="generated-pwd">Cliquez sur Générer</div>
        <button class="gen-btn" onclick="generatePassword()">Générer</button>
        <button onclick="copyPassword()">Copier</button>
        <p style="margin-top:14px; font-size:13px; color:#888;">La méthode des 4 mots : choisissez 4 mots aléatoires et séparez-les par un tiret. Long, mémorable, impossible à casser.</p>
      </div>
    </div>
  </div>
  <script src="script.js"></script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html écrit avec succès !")