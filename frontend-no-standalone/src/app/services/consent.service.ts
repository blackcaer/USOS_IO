import { UserService } from './user.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';
import { Consent } from '../common/consent';
import { Teacher } from '../common/teacher';

@Injectable({
  providedIn: 'root'
})
export class ConsentService {

  constructor(private http: HttpClient,
              private userService: UserService
  ) { }

  private consentUrl: string = "http://localhost:8000/econsent";

  async getPendingConsents(): Promise<Consent[]> {
      const url = `${this.consentUrl}/templates/pending/`;

      try {
        const response: getConsentResponse[] = await lastValueFrom(this.http.get<getConsentResponse[]>(url, { withCredentials: true }));
        return response.map(element => Consent.fromApiResponse(element));
      } catch (error) {
        console.error('Błąd w ładowaniu zgód:', error);
        return [];
      }
    }

    async postParentConsent(consentId: number, data: FormData) {

      this.http.post<any>(`${this.consentUrl}/templates/${consentId}/submit_consent/`, data, {withCredentials: true})
      .subscribe({
        next: (response) => {
          console.log('Plik załadowany:', response);
          alert('Plik załadowany!');
        },
        error: (error) => {
          console.error('Błąd ładowania pliku:', error);
          alert('Niestety plik został nie załadowany!');
        },
      });
    }
  
}

interface getConsentResponse {
  id: number;
  title: string;
  description: string;
  end_date: string;
  author: Teacher;
  parent_submission: boolean;
}

