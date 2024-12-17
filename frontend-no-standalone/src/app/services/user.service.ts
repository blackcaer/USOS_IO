import { Injectable } from '@angular/core';
import { User } from '../common/user';
import { HttpBackend, HttpClient } from '@angular/common/http';
import { lastValueFrom, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private userUrl = 'http://localhost:8000/user';
  private currentUserId = localStorage.getItem('currentUserId');

  constructor(private http: HttpClient) {

  }

  fromApiResponse(response: any): User {
    return new User({
        id: response.id || null,
        first_name: response.first_name,
        last_name: response.last_name,
        username: response.username,
        email: response.email,
        phone_number: response.phone_number || null,
        photo_url: response.photo_url || null,
        birth_date: response.birth_date,
        role: response.role,
        sex: response.sex,
        status: response.status,
        });
    }

    async getAllUserGroups(userId: number): Promise<number[]> {
      const url = `${this.userUrl}/${userId}/student/groups`;
      try {
        const response: getResponseStudentGroup[] = await lastValueFrom(this.http.get<getResponseStudentGroup[]>(url, { withCredentials: true }));
        return response.map(group => group.id);
      } catch (error) {
        console.error('Błąd w ładowaniu groups:', error);
        return [];
      }
    }
  
    async getAllUsersSubjects(userId: number): Promise<Map<number, { id: number, name: string }[]>> {
      const url = `${this.userUrl}/${userId}/student/groups`;
      const userGroups = await this.getAllUserGroups(userId);
      const subjects = new Map<number, { id: number, name: string }[]>();
  
      for (const groupId of userGroups) {
        try {
          const response = await lastValueFrom(this.http.get<getResponseSubject[]>(`${url}/${groupId}/subjects`, { withCredentials: true }));
          const tempSubjects = response.map(element => ({
            id: element.id,
            name: element.subject_name
          }));
          subjects.set(groupId, tempSubjects);

        } catch (error) {
          console.error(`Błęd ładowania danych groupId ${groupId}:`, error);
        }
      }
  
      return subjects;
    }

    async getUsersGradesFromSubject(userId: number, subjectId: number): Promise<string[]> {
      const url = `http://localhost:8000/grades/${userId}/${subjectId}`;
      try {
        const response = await lastValueFrom(this.http.get<getGradeResponse[]>(url, { withCredentials: true }));
        return response.map(element => element.value);

      } catch (error) {
        console.error('Błąd w ładowaniu ocen:', error);
        return [];
      }
    }

    async getUsersGradesFromSubjectWithTimestamp(userId: number, subjectId: number): Promise<{value: string, timestamp: Date}[]> {
      const url = `http://localhost:8000/grades/${userId}/${subjectId}`;
      try {
        const response = await lastValueFrom(this.http.get<getGradeResponse[]>(url, { withCredentials: true }));
        return response.map(element => ({
          value: element.value,
          timestamp: new Date(element.timestamp)
        }));

      } catch (error) {
        console.error('Błąd w ładowaniu ocen:', error);
        return [];
      }
    }

    getUserIdAsInt(): number {
      const storedUserId = localStorage.getItem('currentUserId');
      return storedUserId ? parseInt(storedUserId, 10) : -1;
    }

    parseGradeValue(value: string): number {
      const gradeMap: { [key: string]: number } = {
        'GRADE5': 5,
        'GRADE4': 4,
        'GRADE3': 3,
        'GRADE2': 2,
        'GRADE1': 1
      };
    
      return gradeMap[value] || 0; 
    }
}

interface getResponseSubject {
  id: number;
  subject_name: string;
  description: string;
  is_mandatory: boolean;
  student_group: number;
}

interface getResponseStudentGroup {
  id: number;
  name: string;
  description: string;
  level: number;
  section: string;
  students: number[];
}

interface getGradeResponse {
  id: number;
  value: string;
  timestamp: string;
  student: number;
  grade_column: number;
  count_to_avg: boolean;
}