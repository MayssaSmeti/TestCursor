import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  hasTranscription = false;
  hasDataFile = false;
  hasVisualizations = false;
  hasInsights = false;

  constructor(
    private router: Router,
    private dataService: DataService
  ) { }

  ngOnInit(): void {
    // Vérifier l'état des données
    this.dataService.transcription$.subscribe(transcription => {
      this.hasTranscription = !!transcription;
    });

    this.dataService.dataFilePath$.subscribe(path => {
      this.hasDataFile = !!path;
    });

    this.dataService.visualizations$.subscribe(visualizations => {
      this.hasVisualizations = visualizations && visualizations.length > 0;
    });

    this.dataService.insights$.subscribe(insights => {
      this.hasInsights = !!insights;
    });
  }

  navigateTo(route: string): void {
    this.router.navigate([route]);
  }

  resetAll(): void {
    if (confirm('Êtes-vous sûr de vouloir réinitialiser toutes les données ?')) {
      this.dataService.resetAll();
    }
  }
} 