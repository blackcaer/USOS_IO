import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GradeService {

  private apiUrl = 'http://localhost:3000';

  constructor(private http: HttpClient) {}

  
  getFiveNewestGrades(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + `/grades?student=1`).pipe(
      map((grades) => grades.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()).slice(0, 5))
    )
  }
}
