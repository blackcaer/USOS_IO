import { AuthService } from './services/auth.service';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'USOS';
  showHeader: boolean = true; // Flaga do zarządzania widocznością nagłówka

  constructor(public authService: AuthService, private router: Router) {
    // Nasłuchuje zmian w ścieżkach i aktualizuje widoczność nagłówka
    this.router.events.subscribe(() => {
      this.showHeader = this.router.url !== '/login';
    });
  }

  mainLogout() {
    this.authService.logout();
  }
}
