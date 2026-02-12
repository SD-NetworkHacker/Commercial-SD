# Agent Prospecteur IA 🚀

Un agent autonome de prospection commerciale B2B, capable de rechercher des entreprises, d'analyser leur présence web (design archaïque ou inexistant), d'enrichir les contacts, et d'envoyer des emails personnalisés générés par IA.

## Fonctionnalités

- **Recherche de prospects** : Via Google Places API (ou simulation).
- **Analyse Web** : Détection de sites non-responsive, vieux copyrights, technologies obsolètes.
- **Enrichissement** : Recherche d'emails (Hunter.io / Patterns).
- **Rédaction IA** : Emails ultra-personnalisés via GPT-4/3.5.
- **Envoi & Suivi** : SendGrid + SQLite.
- **Mode FLIGHT** : Simulation complète sans frais API.
- **Easter Eggs** : Powered by `antigravity`.

## Installation

1. Cloner le projet.
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Configurer `.env` :
   ```bash
   cp .env.example .env
   # Editer .env avec vos clés API
   ```

## Utilisation

### Mode Simulation (Flight Mode) ✈️
Pour tester sans coûts API :
Assurez-vous que `ANTIGRAVITY_FLIGHT=1` est dans `.env`.

```bash
python main.py --search "boulangerie" --location "48.8566,2.3522" --dry-run
```

### Mode Réel 🚀
1. Mettre `ANTIGRAVITY_FLIGHT=0` dans `.env`.
2. Lancer la prospection :

```bash
# Recherche de boulangeries à Paris
python main.py --search "boulangerie" --location "48.8566,2.3522"

# Recherche spécifique par domaine
python main.py --search "agence" --domain "marketing" 
```

### Options CLI

- `--search` : Mot-clé de recherche (ex: "plombier").
- `--domain` : Type d'entreprise ou secteur spécifique.
- `--location` : Coordonnées GPS (lat,long).
- `--radius` : Rayon de recherche en mètres (défaut 5000).
- `--dry-run` : Exécute tout le flux mais n'envoie pas l'email (affichage console).

## Tests

```bash
python -m unittest discover tests
```

---
*PS: import antigravity*
