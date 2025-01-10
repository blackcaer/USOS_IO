import { UserService } from './user.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';
import { Consent } from '../common/consent';
import { Teacher } from '../common/teacher';
import { ConsentTemplate } from '../common/consent-template';

@Injectable({
  providedIn: 'root'
})
export class ConsentService {

  constructor(private http: HttpClient,
              private userService: UserService
  ) { }

  private mainUrl2 = 'http://127.0.0.1:8000';
  private mainUrl = 'http://localhost:8000';
  private options = {withCredentials: true, 'access-control-allow-origin': "http://localhost:4200/"};

  private consentUrl: string = this.mainUrl + "/econsent";

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

  async getConsentTemplates(): Promise<ConsentTemplate[]> {
    const url = `${this.consentUrl}/templates/`;

    try {
      const response: getConsentTemplateResponse[] = await lastValueFrom(this.http.get<getConsentTemplateResponse[]>(url, { withCredentials: true }));
      return response.map(element => ConsentTemplate.fromApiResponse(element));
    } catch (error) {
      console.error('Błąd w ładowaniu zgód:', error);
      return [];
    }
  }

  /* async getConsentTemplate(consentId: number): Promise<ConsentTemplate | null> {
    const url = `${this.consentUrl}/templates/${consentId}`;

    try {
      const response: getConsentTemplateResponse = await lastValueFrom(this.http.get<getConsentTemplateResponse>(url, { withCredentials: true }));
      return ConsentTemplate.fromApiResponse(response);
    } catch (error) {
      console.error('Błąd w ładowaniu zgód:', error);
      return null;
    }
  } */

  async postParentConsent(consentId: number, data: FormData) {
    const token = this.userService.getUserToken();
    const headers = new HttpHeaders().set('HTTP_X_XSRF_TOKEN', `${token}`); 

    this.http.post(`${this.consentUrl}/templates/${consentId}/submit_consent/`, data, this.options)
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

  async postConsentTemplate(data: any) {
    this.http.post(`${this.consentUrl}/templates/`, data, this.options)
      .subscribe({
        next: (response) => {
          console.log('Zgoda stworzona:', response);
        },
        error: (error) => {
          console.error('Błąd tworzenia nowej zgody:', error);
        }
      });
  }

  async deleteConsentTemplate(consentTemplateId: number) {
    this.http.delete(`${this.consentUrl}/templates/${consentTemplateId}/`)
      .subscribe({
        next: (response) => {
          console.log('Zgoda została usunięta:', response);
        },
        error: (error) => {
          console.error('Błąd usunięcia zgody:', error);
        }
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

interface getParentConsentResponse {
  id: number;
  parentUser: number;
  childUser: number;
  consent: number;
  isConsent: boolean;
  file: string;
}

interface getConsentTemplateResponse {
  id: number;
  title: string;
  description: string;
  end_date: string;
  students: number[];
  parent_consents: getParentConsentResponse[];
  author: Teacher;
  parent_submission: boolean;
}