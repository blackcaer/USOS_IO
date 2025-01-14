import { filter } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom, Observable } from 'rxjs';
import { ScheduleEvent } from '../common/schedule-event';
import { getScheduleEventResponse } from './user.service';
import { SchoolSubject } from '../common/school-subject';
import { GradeColumn } from '../common/grade-column';

@Injectable({
  providedIn: 'root'
})
export class MeetingService {

  private mainUrl2 = 'http://127.0.0.1:8000';
  private mainUrl = 'http://localhost:8000';
  private options = {withCredentials: true, 'access-control-allow-origin': "http://localhost:4200/"};
  private apiUrl = this.mainUrl + '/meetings/';

  constructor(private http: HttpClient) { }

  createMeeting(meetingData: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, meetingData, this.options);
  }

  async getTeachersSubjectsBySubstring(substring: string): Promise<SchoolSubject[]> {
    const url = `${this.mainUrl}/meetings/schedule/`;
    try {
      const response = await lastValueFrom(this.http.get<getScheduleEventResponse[]>(url, { withCredentials: true }));
      const uniqueSubjects = new Set<number>();
  
      return response
        .filter(event => {
          const subjectKey = event.school_subject.id;
          if (event.school_subject.student_group.name === substring && !uniqueSubjects.has(subjectKey)) {
            uniqueSubjects.add(subjectKey);
            return true;
          }
          return false;
        })
        .map(event => SchoolSubject.fromApiResponse(event.school_subject)); // Преобразуем только уникальные предметы
    } catch (error) {
      console.error('Błąd w ładowaniu przedmiotów nauczyciela:', error);
      return [];
    }
  }

  /* async getGradeColumn(columnId: number): Promise<GradeColumn | null> {
    const url = `${this.mainUrl}/meetings/schedule/`;

    try {
      const response = await lastValueFrom(this.http.get<getGradeColumnResponse>(url, { withCredentials: true }));
      return GradeColumn.fromApiResponse(response);
    }
    catch (error) {
      console.error('Błąd w ładowaniu przedmiotów nauczyciela:', error);
      return null;
    }
    
  } */

  async getSubjectsGradeColumns(subject: SchoolSubject): Promise<GradeColumn[]> {
    const url = `${this.mainUrl}/grade-columns/`;

    try {
      const response = await lastValueFrom(this.http.get<getGradeColumnResponse[]>(url, { withCredentials: true }));
      return response.filter((gradeColumn) => gradeColumn.school_subject === subject.id).map((gradeColumn) => GradeColumn.fromApiResponse(gradeColumn));
    } catch (error) {
      console.error('Błąd w ładowaniu tematów:', error);
      return [];
    }
  }

  postGrade(gradeData: any, studentId: number, subjectId: number): Observable<any> {
    const gradeUrl = `${this.mainUrl}/grades/${studentId}/${subjectId}/`

    return this.http.post<any>(gradeUrl, gradeData, this.options);
  }
}

export interface getGradeColumnResponse {
  id: number;
  title: string;
  weight: number;
  description: string;
  school_subject: number;
}