import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = '/api';

  constructor(private http: HttpClient) { }

  // Enregistrement audio
  uploadAudio(audioFile: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', audioFile);
    
    return this.http.post(`${this.apiUrl}/upload_audio`, formData);
  }

  // Transcription audio
  transcribeAudio(filepath: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/transcribe_audio`, { filepath });
  }

  // Analyse de texte
  analyzeText(text: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/analyze_text`, { text });
  }

  // Upload de fichier de données
  uploadDataFile(dataFile: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', dataFile);
    
    return this.http.post(`${this.apiUrl}/upload_data_file`, formData);
  }

  // Génération de visualisations
  generateVisualizations(filepath: string, vizType: string = 'auto', analysis: string = ''): Observable<any> {
    return this.http.post(`${this.apiUrl}/generate_visualization`, {
      filepath,
      visualization_type: vizType,
      analysis
    });
  }

  // Génération d'insights
  generateInsights(filepath: string, transcript: string = '', analysis: string = ''): Observable<any> {
    return this.http.post(`${this.apiUrl}/generate_insights`, {
      filepath,
      transcript,
      analysis
    });
  }
} 