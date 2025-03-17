import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { AudioRecorderService } from '../../services/audio-recorder.service';
import { ApiService } from '../../services/api.service';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-audio-recorder',
  templateUrl: './audio-recorder.component.html',
  styleUrls: ['./audio-recorder.component.css']
})
export class AudioRecorderComponent implements OnInit, OnDestroy {
  isRecording = false;
  audioUrl: string | null = null;
  recordingTime = 0;
  timerInterval: any;
  errorMessage = '';
  isUploading = false;
  isTranscribing = false;
  isAnalyzing = false;
  transcriptionText = '';
  analysisText = '';
  
  private subscriptions: Subscription[] = [];

  constructor(
    private router: Router,
    private audioRecorderService: AudioRecorderService,
    private apiService: ApiService,
    private dataService: DataService
  ) { }

  ngOnInit(): void {
    // S'abonner aux changements d'état de l'enregistrement
    this.subscriptions.push(
      this.audioRecorderService.recordingStatus$.subscribe(status => {
        this.isRecording = status;
        if (status) {
          this.startTimer();
        } else {
          this.stopTimer();
        }
      })
    );

    // S'abonner à l'URL de l'audio
    this.subscriptions.push(
      this.audioRecorderService.audioUrl$.subscribe(url => {
        this.audioUrl = url;
      })
    );
  }

  ngOnDestroy(): void {
    // Nettoyer les abonnements
    this.subscriptions.forEach(sub => sub.unsubscribe());
    this.stopTimer();
  }

  startRecording(): void {
    this.errorMessage = '';
    this.audioRecorderService.startRecording().catch(error => {
      this.errorMessage = `Erreur lors de l'accès au microphone: ${error.message}`;
      console.error('Erreur de démarrage de l\'enregistrement:', error);
    });
    this.dataService.setProcessState('recording', true);
  }

  stopRecording(): void {
    this.audioRecorderService.stopRecording();
    this.dataService.setProcessState('recording', false);
  }

  clearRecording(): void {
    this.audioRecorderService.clearRecording();
    this.recordingTime = 0;
    this.transcriptionText = '';
    this.analysisText = '';
    this.errorMessage = '';
  }

  async uploadAndTranscribe(): Promise<void> {
    const audioBlob = await this.audioRecorderService.audioBlob$.toPromise();
    
    if (!audioBlob) {
      this.errorMessage = 'Aucun enregistrement audio disponible.';
      return;
    }

    try {
      // Créer un fichier à partir du blob
      const audioFile = this.audioRecorderService.createAudioFileFromBlob(audioBlob);
      
      // Mettre à jour l'état
      this.isUploading = true;
      this.dataService.setProcessState('uploading', true);
      
      // Télécharger le fichier audio
      const uploadResponse = await this.apiService.uploadAudio(audioFile).toPromise();
      
      if (!uploadResponse.success) {
        throw new Error(uploadResponse.error || 'Erreur lors du téléchargement de l\'audio');
      }
      
      // Sauvegarder le chemin du fichier
      this.dataService.setAudioFilePath(uploadResponse.filepath);
      
      // Mettre à jour l'état
      this.isUploading = false;
      this.isTranscribing = true;
      this.dataService.setProcessState('uploading', false);
      this.dataService.setProcessState('transcribing', true);
      
      // Transcrire l'audio
      const transcriptionResponse = await this.apiService.transcribeAudio(uploadResponse.filepath).toPromise();
      
      if (!transcriptionResponse.success) {
        throw new Error(transcriptionResponse.error || 'Erreur lors de la transcription');
      }
      
      // Sauvegarder la transcription
      this.transcriptionText = transcriptionResponse.transcript;
      this.dataService.setTranscription(transcriptionResponse.transcript);
      
      // Mettre à jour l'état
      this.isTranscribing = false;
      this.isAnalyzing = true;
      this.dataService.setProcessState('transcribing', false);
      this.dataService.setProcessState('analyzing', true);
      
      // Analyser le texte
      const analysisResponse = await this.apiService.analyzeText(transcriptionResponse.transcript).toPromise();
      
      if (!analysisResponse.success) {
        throw new Error(analysisResponse.error || 'Erreur lors de l\'analyse');
      }
      
      // Sauvegarder l'analyse
      this.analysisText = analysisResponse.analysis;
      this.dataService.setAnalysis(analysisResponse.analysis);
      
      // Terminer
      this.isAnalyzing = false;
      this.dataService.setProcessState('analyzing', false);
      
    } catch (error) {
      console.error('Erreur lors du traitement de l\'audio:', error);
      this.errorMessage = `Erreur: ${error.message}`;
      
      // Réinitialiser les états
      this.isUploading = false;
      this.isTranscribing = false;
      this.isAnalyzing = false;
      this.dataService.setProcessState('uploading', false);
      this.dataService.setProcessState('transcribing', false);
      this.dataService.setProcessState('analyzing', false);
    }
  }

  navigateToTranscription(): void {
    this.router.navigate(['/transcription']);
  }

  private startTimer(): void {
    this.recordingTime = 0;
    this.timerInterval = setInterval(() => {
      this.recordingTime++;
    }, 1000);
  }

  private stopTimer(): void {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }

  formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
} 