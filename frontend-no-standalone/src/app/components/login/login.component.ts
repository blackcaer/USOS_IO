import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { CookieService } from '../../services/cookie.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  loginForm: FormGroup;
  message: string = '';
  messageType: 'success' | 'error' = 'success';

  constructor(private fb: FormBuilder, private http: HttpClient, private router: Router, private cookieService: CookieService) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      // const csrfToken = this.cookieService.getCookie('XSRF-TOKEN');
      // const headers = new HttpHeaders().set('HTTP_X_XSRF_TOKEN', csrfToken);
      const formData = new FormData();
      formData.append('username', this.loginForm.get('username')?.value);
      formData.append('password', this.loginForm.get('password')?.value);

      this.http.post('http://localhost:8000/auth/login/', formData, { withCredentials: true }).subscribe({
        next: (response: any) => {
          if (response.csrftoken) {
            localStorage.setItem('csrftoken', response.csrftoken);
          }
          if (response.sessionid) {
            localStorage.setItem('sessionid', response.sessionid);
          }
          this.message = 'Вход выполнен успешно!';
          this.messageType = 'success';
          this.router.navigate(['/']);
        },
        error: (error) => {
          this.message = error.error?.detail || 'Ошибка входа';
          this.messageType = 'error';
        }
      });
    } else {
      this.message = 'Пожалуйста, заполните все поля формы.';
      this.messageType = 'error';
    }
  }
}




