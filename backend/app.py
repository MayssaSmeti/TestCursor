from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import base64
from io import BytesIO
import openai
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from werkzeug.utils import secure_filename
import io
import PyPDF2
import json
import traceback

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Activation de CORS pour permettre les requêtes depuis Angular

# Configuration des dossiers
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'xlsx', 'xls', 'csv', 'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuration de l'API OpenAI
openai.api_key = "YOUR_OPENAI_API_KEY"  # Remplacez par votre clé API

# Palette de couleurs personnalisée
CUSTOM_COLORS = ['#d85218', '#f0aa2c', '#ac1c04', '#286454', '#280458', '#2c0404']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    """Endpoint pour recevoir et sauvegarder un fichier audio"""
    
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier trouvé'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
    if file and allowed_file(file.filename):
        # Génère un nom de fichier unique
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath
        })
    
    return jsonify({'error': 'Type de fichier non autorisé'}), 400

@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    """Endpoint pour transcrire un fichier audio à l'aide de l'API OpenAI Whisper"""
    
    data = request.get_json()
    filepath = data.get('filepath')
    
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'Fichier audio introuvable'}), 400
    
    try:
        # Ouvrir le fichier audio
        with open(filepath, "rb") as audio_file:
            # Transcription via l'API OpenAI Whisper
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        return jsonify({
            'success': True,
            'transcript': transcript.text
        })
    except Exception as e:
        print(f"Erreur de transcription: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f'Erreur de transcription: {str(e)}'}), 500

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    """Endpoint pour analyser le texte transcrit avec l'API OpenAI"""
    
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'Aucun texte fourni pour analyse'}), 400
    
    try:
        # Analyse du texte via l'API OpenAI
        response = openai.chat.completions.create(
            model="gpt-4",  # Ou un autre modèle approprié
            messages=[
                {"role": "system", "content": "Tu es un assistant d'analyse de données. Extrais les principales requêtes et intentions de l'utilisateur concernant l'analyse de données."},
                {"role": "user", "content": text}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        analysis = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        print(f"Erreur d'analyse: {str(e)}")
        return jsonify({'error': f'Erreur d\'analyse: {str(e)}'}), 500

@app.route('/upload_data_file', methods=['POST'])
def upload_data_file():
    """Endpoint pour recevoir et traiter un fichier de données (Excel, CSV, PDF)"""
    
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier trouvé'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
    if file and allowed_file(file.filename):
        # Génère un nom de fichier unique
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Traitement du fichier selon son type
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        
        try:
            if file_ext in ['xlsx', 'xls']:
                # Traitement des fichiers Excel
                df = pd.read_excel(filepath)
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'filepath': filepath,
                    'columns': df.columns.tolist(),
                    'data': df.head(100).to_dict(orient='records'),
                    'info': {
                        'rows': len(df),
                        'columns': len(df.columns)
                    }
                })
                
            elif file_ext == 'csv':
                # Traitement des fichiers CSV
                df = pd.read_csv(filepath)
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'filepath': filepath,
                    'columns': df.columns.tolist(),
                    'data': df.head(100).to_dict(orient='records'),
                    'info': {
                        'rows': len(df),
                        'columns': len(df.columns)
                    }
                })
                
            elif file_ext == 'pdf':
                # Traitement des fichiers PDF (extraction de texte)
                text_content = []
                with open(filepath, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    num_pages = len(pdf_reader.pages)
                    
                    for page_num in range(num_pages):
                        page = pdf_reader.pages[page_num]
                        text_content.append(page.extract_text())
                
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'filepath': filepath,
                    'text_content': text_content,
                    'info': {
                        'pages': num_pages
                    }
                })
                
        except Exception as e:
            print(f"Erreur de traitement du fichier: {str(e)}")
            return jsonify({'error': f'Erreur de traitement du fichier: {str(e)}'}), 500
    
    return jsonify({'error': 'Type de fichier non autorisé'}), 400

@app.route('/generate_visualization', methods=['POST'])
def generate_visualization():
    """Endpoint pour générer des visualisations à partir des données et de l'analyse"""
    
    data = request.get_json()
    
    viz_type = data.get('visualization_type', 'auto')
    file_path = data.get('filepath')
    analysis = data.get('analysis', '')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'Fichier de données introuvable'}), 400
    
    try:
        # Chargement des données
        file_ext = file_path.rsplit('.', 1)[1].lower()
        
        if file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(file_path)
        elif file_ext == 'csv':
            df = pd.read_csv(file_path)
        else:
            return jsonify({'error': 'Format de fichier non pris en charge pour les visualisations'}), 400
        
        # Génération de visualisations en fonction de l'analyse
        visualizations = generate_visualizations(df, viz_type, analysis)
        
        return jsonify({
            'success': True,
            'visualizations': visualizations
        })
        
    except Exception as e:
        print(f"Erreur de génération de visualisation: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f'Erreur de génération de visualisation: {str(e)}'}), 500

def generate_visualizations(df, viz_type='auto', analysis=''):
    """Génère plusieurs visualisations basées sur les types de données et l'analyse"""
    
    visualizations = []
    
    # Configuration de la palette de couleurs personnalisée
    sns.set_palette(CUSTOM_COLORS)
    
    # Analyse de l'intention de l'utilisateur grâce à l'API OpenAI
    if analysis:
        try:
            # Utilisation de l'API pour déterminer les meilleures visualisations
            prompt = f"""
            Analyse les données suivantes avec ces colonnes: {', '.join(df.columns.tolist())}
            et quelques exemples de données: {df.head(3).to_dict(orient='records')}
            
            Voici une analyse de la demande de l'utilisateur: {analysis}
            
            Retourne un JSON avec une liste de 2-3 visualisations recommandées au format suivant:
            [
                {{
                    "type": "bar|pie|line|scatter|histogram|heatmap",
                    "title": "Titre descriptif",
                    "x_column": "nom_colonne_x",  # Pour les graphiques qui en ont besoin
                    "y_column": "nom_colonne_y",  # Pour les graphiques qui en ont besoin
                    "column": "nom_colonne",  # Pour les graphiques à une variable
                    "description": "Pourquoi cette visualisation est pertinente"
                }}
            ]
            
            N'inclus aucun commentaire ou texte supplémentaire, uniquement le JSON.
            """
            
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un expert en visualisation de données."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            recommendations = json.loads(response.choices[0].message.content)
            
            for rec in recommendations:
                try:
                    plt.figure(figsize=(8, 6))
                    
                    viz_type = rec.get('type')
                    title = rec.get('title')
                    
                    if viz_type == 'bar':
                        x_col = rec.get('x_column')
                        y_col = rec.get('y_column')
                        if x_col in df.columns and y_col in df.columns:
                            sns.barplot(x=df[x_col], y=df[y_col], palette=CUSTOM_COLORS)
                            plt.title(title)
                            plt.xticks(rotation=45)
                    
                    elif viz_type == 'pie':
                        col = rec.get('column')
                        if col in df.columns:
                            plt.figure(figsize=(8, 8))
                            values = df[col].value_counts().head(6)
                            plt.pie(values, labels=values.index, autopct='%1.1f%%', colors=CUSTOM_COLORS)
                            plt.title(title)
                    
                    elif viz_type == 'line':
                        x_col = rec.get('x_column')
                        y_col = rec.get('y_column')
                        if x_col in df.columns and y_col in df.columns:
                            plt.plot(df[x_col], df[y_col], color=CUSTOM_COLORS[0], marker='o')
                            plt.grid(True, linestyle='--', alpha=0.7)
                            plt.title(title)
                    
                    elif viz_type == 'scatter':
                        x_col = rec.get('x_column')
                        y_col = rec.get('y_column')
                        if x_col in df.columns and y_col in df.columns:
                            sns.scatterplot(x=df[x_col], y=df[y_col], color=CUSTOM_COLORS[0])
                            plt.title(title)
                    
                    elif viz_type == 'histogram':
                        col = rec.get('column')
                        if col in df.columns:
                            sns.histplot(df[col], kde=True, color=CUSTOM_COLORS[0])
                            plt.title(title)
                    
                    elif viz_type == 'heatmap':
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        if len(numeric_cols) > 1:
                            corr = df[numeric_cols].corr()
                            sns.heatmap(corr, annot=True, cmap='YlOrRd')
                            plt.title(title)
                    
                    plt.tight_layout()
                    
                    # Sauvegarde de la figure
                    buf = BytesIO()
                    plt.savefig(buf, format='png')
                    plt.close()
                    buf.seek(0)
                    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                    
                    visualizations.append({
                        'type': viz_type,
                        'title': title,
                        'image': img_base64,
                        'description': rec.get('description', '')
                    })
                    
                except Exception as inner_e:
                    print(f"Erreur lors de la génération d'une visualisation recommandée: {str(inner_e)}")
                    continue
                    
        except Exception as e:
            print(f"Erreur lors de la génération des recommandations: {str(e)}")
            # En cas d'échec, on continue avec la génération automatique
    
    # Si aucune visualisation n'a été générée par l'analyse ou si viz_type est 'auto'
    if not visualizations or viz_type == 'auto':
        # Pour les colonnes numériques
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_cols) >= 1:
            # Histogramme pour chaque colonne numérique
            for col in numeric_cols[:3]:  # Limite aux 3 premières colonnes
                plt.figure(figsize=(6, 4))
                sns.histplot(df[col], kde=True, color=CUSTOM_COLORS[0])
                plt.title(f'Distribution de {col}')
                plt.tight_layout()
                buf = BytesIO()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)
                img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                visualizations.append({
                    'type': 'histogram',
                    'title': f'Distribution de {col}',
                    'image': img_base64,
                    'column': col,
                    'description': f"Distribution des valeurs pour la colonne {col}"
                })
            
            # Matrice de corrélation si plusieurs colonnes numériques
            if len(numeric_cols) > 1:
                plt.figure(figsize=(8, 6))
                sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='YlOrRd')
                plt.title('Matrice de Corrélation')
                plt.tight_layout()
                buf = BytesIO()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)
                img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                visualizations.append({
                    'type': 'heatmap',
                    'title': 'Matrice de Corrélation',
                    'image': img_base64,
                    'description': "Visualisation des corrélations entre les variables numériques"
                })
        
        # Pour les colonnes catégorielles
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if len(cat_cols) >= 1:
            for col in cat_cols[:2]:  # Limite aux 2 premières colonnes
                plt.figure(figsize=(7, 5))
                value_counts = df[col].value_counts()
                # Limite aux 10 premières catégories s'il y en a trop
                if len(value_counts) > 10:
                    value_counts = value_counts.head(10)
                sns.barplot(x=value_counts.index, y=value_counts.values, palette=CUSTOM_COLORS)
                plt.title(f'Décompte de {col}')
                plt.xticks(rotation=45)
                plt.tight_layout()
                buf = BytesIO()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)
                img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                visualizations.append({
                    'type': 'barplot',
                    'title': f'Décompte de {col}',
                    'image': img_base64,
                    'column': col,
                    'description': f"Répartition des valeurs pour la colonne catégorielle {col}"
                })
    
    return visualizations

@app.route('/generate_insights', methods=['POST'])
def generate_insights():
    """Endpoint pour générer des insights à partir des données et de la transcription"""
    
    data = request.get_json()
    
    file_path = data.get('filepath')
    transcript = data.get('transcript', '')
    analysis = data.get('analysis', '')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'Fichier de données introuvable'}), 400
    
    try:
        # Chargement des données
        file_ext = file_path.rsplit('.', 1)[1].lower()
        
        if file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(file_path)
        elif file_ext == 'csv':
            df = pd.read_csv(file_path)
        else:
            return jsonify({'error': 'Format de fichier non pris en charge pour les insights'}), 400
        
        # Génération d'insights via l'API OpenAI
        prompt = f"""
        Analyse le jeu de données suivant:
        
        Colonnes: {', '.join(df.columns.tolist())}
        Aperçu des données: {df.head(5).to_dict(orient='records')}
        Statistiques descriptives: {df.describe().to_dict()}
        
        Voici la transcription de la demande de l'utilisateur: {transcript}
        
        Analyse de la demande: {analysis}
        
        Génère un rapport détaillé présentant:
        1. Une synthèse des principales caractéristiques du jeu de données
        2. Des insights pertinents par rapport à la demande de l'utilisateur
        3. Des recommandations pour approfondir l'analyse
        
        Format: Points clés, faciles à lire, concis mais informatifs.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en analyse de données. Tu fournis des insights clairs, pertinents et directement exploitables."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.4
        )
        
        insights = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'insights': insights
        })
        
    except Exception as e:
        print(f"Erreur de génération d'insights: {str(e)}")
        return jsonify({'error': f'Erreur de génération d\'insights: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 