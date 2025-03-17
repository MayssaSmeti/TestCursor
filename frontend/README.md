# Frontend DataSpeak

Ce frontend Angular gère l'interface utilisateur pour l'application DataSpeak, permettant l'enregistrement audio, la transcription, l'analyse de texte et la génération de visualisations.

## Fonctionnalités

- Enregistrement audio via le microphone du navigateur
- Affichage et édition de la transcription
- Téléchargement de fichiers de données (Excel, CSV, PDF)
- Visualisation des données et insights générés

## Configuration requise

- Node.js 14.x ou supérieur
- Angular CLI 16.x
- Les dépendances listées dans `package.json`

## Installation

1. Cloner le dépôt
2. Naviguer vers le dossier frontend
3. Installer les dépendances :
   ```
   npm install
   ```

## Démarrage du serveur de développement

```
npm start
```

L'application sera accessible sur `http://localhost:4200`

## Structure du projet

- `/src/app/components` : Composants Angular
  - `/audio-recorder` : Enregistrement audio
  - `/transcription` : Affichage et édition de la transcription
  - `/data-upload` : Téléchargement de fichiers de données
  - `/visualization` : Affichage des visualisations
  - `/dashboard` : Page d'accueil
- `/src/app/services` : Services Angular
  - `api.service.ts` : Communication avec le backend
  - `audio-recorder.service.ts` : Gestion de l'enregistrement audio
  - `data.service.ts` : Partage de données entre composants

## Proxy

Le fichier `proxy.conf.json` configure le proxy pour rediriger les requêtes API vers le backend Flask sur le port 5000. 