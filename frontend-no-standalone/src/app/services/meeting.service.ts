import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MeetingService {

  private mainUrl2 = 'http://127.0.0.1:8000';
  private mainUrl = 'http://localhost:8000';
  private options = {withCredentials: true, 'access-control-allow-origin': "http://localhost:4200/"};
  private apiUrl = this.mainUrl + '/meetings/';

  constructor(private http: HttpClient) { }

/*   options = {withCredentials: true, 'access-control-allow-origin': "http://localhost:4200/", 'Content-Type': 'application/json'}; */

  createMeeting(meetingData: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, meetingData, this.options);
  }
}
