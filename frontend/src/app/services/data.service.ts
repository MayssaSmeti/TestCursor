import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  // État de la transcription
  private transcriptionSubject = new BehaviorSubject<string>('');
  public transcription$ = this.transcriptionSubject.asObservable();
  
  // État du fichier audio
  private audioFilePathSubject = new BehaviorSubject<string>('');
  public audioFilePath$ = this.audioFilePathSubject.asObservable();
  
  // État de l'analyse
  private analysisSubject = new BehaviorSubject<string>('');
  public analysis$ = this.analysisSubject.asObservable();
  
  // État du fichier de données
  private dataFilePathSubject = new BehaviorSubject<string>('');
  public dataFilePath$ = this.dataFilePathSubject.asObservable();
  
  // Métadonnées du fichier
  private dataFileMetadataSubject = new BehaviorSubject<any>(null);
  public dataFileMetadata$ = this.dataFileMetadataSubject.asObservable();
  
  // Visualisations
  private visualizationsSubject = new BehaviorSubject<any[]>([]);
  public visualizations$ = this.visualizationsSubject.asObservable();
  
  // Insights
  private insightsSubject = new BehaviorSubject<string>('');
  public insights$ = this.insightsSubject.asObservable();
  
  // État du processus (pour afficher les indicateurs de chargement)
  private processStateSubject = new BehaviorSubject<{[key: string]: boolean}>({
    recording: false,
    transcribing: false,
    analyzing: false,
    uploading: false,
    generating: false
  });
  public processState$ = this.processStateSubject.asObservable();

  constructor() { }

  // Setters
  setTranscription(transcription: string): void {
    this.transcriptionSubject.next(transcription);
  }

  setAudioFilePath(path: string): void {
    this.audioFilePathSubject.next(path);
  }

  setAnalysis(analysis: string): void {
    this.analysisSubject.next(analysis);
  }

  setDataFilePath(path: string): void {
    this.dataFilePathSubject.next(path);
  }

  setDataFileMetadata(metadata: any): void {
    this.dataFileMetadataSubject.next(metadata);
  }

  setVisualizations(visualizations: any[]): void {
    this.visualizationsSubject.next(visualizations);
  }

  setInsights(insights: string): void {
    this.insightsSubject.next(insights);
  }

  // Méthodes d'état du processus
  setProcessState(state: string, value: boolean): void {
    const currentState = this.processStateSubject.value;
    this.processStateSubject.next({ ...currentState, [state]: value });
  }

  // Réinitialiser tous les états
  resetAll(): void {
    this.transcriptionSubject.next('');
    this.audioFilePathSubject.next('');
    this.analysisSubject.next('');
    this.dataFilePathSubject.next('');
    this.dataFileMetadataSubject.next(null);
    this.visualizationsSubject.next([]);
    this.insightsSubject.next('');
    this.processStateSubject.next({
      recording: false,
      transcribing: false,
      analyzing: false,
      uploading: false,
      generating: false
    });
  }

  // Getters actuels
  getCurrentTranscription(): string {
    return this.transcriptionSubject.value;
  }

  getCurrentAudioFilePath(): string {
    return this.audioFilePathSubject.value;
  }

  getCurrentAnalysis(): string {
    return this.analysisSubject.value;
  }

  getCurrentDataFilePath(): string {
    return this.dataFilePathSubject.value;
  }

  getCurrentDataFileMetadata(): any {
    return this.dataFileMetadataSubject.value;
  }

  getCurrentVisualizations(): any[] {
    return this.visualizationsSubject.value;
  }

  getCurrentInsights(): string {
    return this.insightsSubject.value;
  }
} 