# Backend DataSpeak

Ce backend Flask gère le traitement audio, la transcription, l'analyse de texte et la génération de visualisations pour l'application DataSpeak.

## Fonctionnalités

- Enregistrement et traitement des fichiers audio
- Transcription audio en texte via OpenAI Whisper
- Analyse du texte transcrit via OpenAI GPT
- Traitement de fichiers de données (Excel, CSV, PDF)
- Génération de visualisations personnalisées et insights

## Configuration requise

- Python 3.8 ou supérieur
- Les dépendances listées dans `requirements.txt`
- Une clé API OpenAI valide

## Installation

1. Cloner le dépôt
2. Naviguer vers le dossier backend
3. Installer les dépendances :
   ```
   pip install -r requirements.txt
   ```
4. Créer un fichier `.env` avec votre clé API OpenAI :
   ```
   OPENAI_API_KEY=votre_cle_api_openai
   ```

## Démarrage du serveur

```
python app.py
```

Le serveur démarrera sur `http://localhost:5000`

## API Endpoints

- POST `/upload_audio` : Télécharger un fichier audio
- POST `/transcribe_audio` : Transcrire un fichier audio en texte
- POST `/analyze_text` : Analyser le texte pour extraire les intentions
- POST `/upload_data_file` : Télécharger et traiter un fichier de données
- POST `/generate_visualization` : Générer des visualisations
- POST `/generate_insights` : Générer des insights basés sur les données et la transcription

## Structure des dossiers

- `/uploads` : Stockage des fichiers téléchargés
- `/static` : Ressources statiques 