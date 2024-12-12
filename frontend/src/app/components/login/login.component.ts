import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {
  loginForm: FormGroup;
  message: string = '';
  messageType: 'success' | 'error' = 'success';

  constructor(private fb: FormBuilder, private http: HttpClient, private router: Router) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.http.post('http://localhost:8000/auth/login/', this.loginForm.value).subscribe({
        next: (response: any) => {
          this.message = 'Login successful!';
          this.messageType = 'success';
          localStorage.setItem('token', response.token);
          this.router.navigate(['']);
        },
        error: (error: any) => {
          this.message = error.error?.error || 'Login failed!';
          this.messageType = 'error';
        }
      });
    } else {
      this.message = 'Please fill out the form correctly.';
      this.messageType = 'error';
    }
  }
}