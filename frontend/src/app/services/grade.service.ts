import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { SchoolSubject } from '../common/school-subject';

@Injectable({
  providedIn: 'root'
})
export class GradeService {

  private baseUrl = 'http://localhost:3000';

  constructor(private httpClient: HttpClient) {}


  getStudentSubject(studentId: number) : Observable<SchoolSubject[]> {

    const subjectsUrl: string = this.baseUrl + `/schoolSubjects`;

    return this.httpClient.get<SchoolSubject[]>(subjectsUrl);
  }
  
  /*
  getFiveNewestGrades(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + `/grades?student=1`).pipe(
      map((grades) => grades.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()).slice(0, 5))
    )
  }
  */
}
