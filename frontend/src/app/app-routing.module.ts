import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { AudioRecorderComponent } from './components/audio-recorder/audio-recorder.component';
import { TranscriptionComponent } from './components/transcription/transcription.component';
import { DataUploadComponent } from './components/data-upload/data-upload.component';
import { VisualizationComponent } from './components/visualization/visualization.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'record', component: AudioRecorderComponent },
  { path: 'transcription', component: TranscriptionComponent },
  { path: 'data-upload', component: DataUploadComponent },
  { path: 'visualization', component: VisualizationComponent },
  { path: '**', redirectTo: '/dashboard' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { } 