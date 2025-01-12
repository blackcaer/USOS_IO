import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { CookieService } from './cookie.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private mainUrl2 = 'http://127.0.0.1:8000';
  private mainUrl = 'http://localhost:8000';
  private options = {withCredentials: true, 'access-control-allow-origin': "http://localhost:4200/"};
  private loginUrl = this.mainUrl + '/auth/login/';

  constructor(private router: Router,
              private http: HttpClient, 
              private cookieService: CookieService
  ) { }

  login(username: string, password: string): Observable<any> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    return new Observable((observer) => {
      this.http.post(this.loginUrl, formData, this.options).subscribe({
        next: (response: any) => {
          const xsrfToken = this.cookieService.getCookie('XSRF_TOKEN');
          const sessionid = this.cookieService.getCookie('sessionid');

          if (!!response.role) {
            localStorage.setItem('currentUserRole', response.role);
            console.log(response);
          }
          if (!!response.id) {
            localStorage.setItem('currentUserId', response.id);
          }
          if (!!xsrfToken) {
            localStorage.setItem('xsrftoken', xsrfToken);
          }
          if (!!sessionid) {
            localStorage.setItem('sessionid', sessionid);
          }

          observer.next(response);
          observer.complete();
        },
        error: (error) => {
          observer.error(error);
        },
      });
    });
  }

  logout() {
    localStorage.removeItem('xsrftoken');
    localStorage.removeItem('sessionid');
    localStorage.removeItem('currentUserId');
    localStorage.removeItem('currentUserRole');
    this.router.navigate(['/login']);
  }

  isLoggedIn(): boolean {
    const xsrfToken = localStorage.getItem('xsrftoken');
    const sessionId = localStorage.getItem('sessionid');
    const currentUserId = localStorage.getItem('currentUserId');
    const currentUserRole = localStorage.getItem('currentUserRole');
    return !!xsrfToken && !!sessionId && !!currentUserId && !!currentUserRole;
  }
}


