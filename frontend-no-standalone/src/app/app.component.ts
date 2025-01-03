import { AuthService } from './services/auth.service';
import { Component } from '@angular/core';
import { Router,NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'USOS';
  showHeader: boolean = true; // Flaga do zarządzania widocznością nagłówka

  constructor(public authService: AuthService, private router: Router) {
    this.router.events
      .pipe(
        filter((event): event is NavigationEnd => event instanceof NavigationEnd) // Wymuszamy typowanie
      )
      .subscribe((event: NavigationEnd) => {
        // Sprawdź, czy URL zaczyna się od '/login'
        this.showHeader = !event.url.startsWith('/login');
      });
  }

  mainLogout() {
    this.authService.logout();
  }
}
