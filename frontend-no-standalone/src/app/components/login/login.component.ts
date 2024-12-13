import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { CookieService } from '../../services/cookie.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  loginForm: FormGroup;
  message: string = '';
  messageType: 'success' | 'error' = 'success';

  constructor(private fb: FormBuilder,
              private http: HttpClient,
              private router: Router,
              private cookieService: CookieService,
              private authService: AuthService,) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const username = this.loginForm.get('username')?.value;
      const password = this.loginForm.get('password')?.value;

      this.authService.login(username, password).subscribe({
        next: (response: any) => {
<<<<<<< Updated upstream
=======
          console.log(response);
>>>>>>> Stashed changes
          this.message = 'Logowanie się udało';
          this.messageType = 'success';
          this.router.navigate(['/']);
        },
        error: (error) => {
          this.message = error.error?.detail || 'Wpisane nieprawidłowe dane';
          this.messageType = 'error';
        },
      });
    } else {
      this.message = 'Wszystkie pola muszą być wypełnieni';
      this.messageType = 'error';
    }
  }
}




