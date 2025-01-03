import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MeetingService {

  private apiUrl = 'http://127.0.0.1:8000/meetings/';

  constructor(private http: HttpClient) { }

  createMeeting(meetingData: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, meetingData, { withCredentials: true });
  }
}
