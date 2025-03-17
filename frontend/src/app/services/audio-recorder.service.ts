import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AudioRecorderService {
  private mediaRecorder: MediaRecorder | null = null;
  private audioChunks: Blob[] = [];
  
  private recordingStatusSubject = new BehaviorSubject<boolean>(false);
  public recordingStatus$ = this.recordingStatusSubject.asObservable();
  
  private audioUrlSubject = new BehaviorSubject<string | null>(null);
  public audioUrl$ = this.audioUrlSubject.asObservable();
  
  private audioBlobSubject = new BehaviorSubject<Blob | null>(null);
  public audioBlob$ = this.audioBlobSubject.asObservable();

  constructor() { }

  public async startRecording(): Promise<void> {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.audioChunks = [];
      
      this.mediaRecorder.addEventListener('dataavailable', event => {
        this.audioChunks.push(event.data);
      });
      
      this.mediaRecorder.addEventListener('stop', () => {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        
        this.audioUrlSubject.next(audioUrl);
        this.audioBlobSubject.next(audioBlob);
        this.recordingStatusSubject.next(false);
        
        // Arrêter tous les tracks audio pour libérer les ressources
        stream.getTracks().forEach(track => track.stop());
      });
      
      this.mediaRecorder.start();
      this.recordingStatusSubject.next(true);
    } catch (error) {
      console.error('Erreur lors du démarrage de l\'enregistrement:', error);
      this.recordingStatusSubject.next(false);
    }
  }

  public stopRecording(): void {
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop();
    }
  }

  public clearRecording(): void {
    this.audioUrlSubject.next(null);
    this.audioBlobSubject.next(null);
  }

  public isRecording(): boolean {
    return this.recordingStatusSubject.value;
  }

  public createAudioFileFromBlob(blob: Blob, filename: string = 'audio.wav'): File {
    return new File([blob], filename, { type: 'audio/wav' });
  }
} 