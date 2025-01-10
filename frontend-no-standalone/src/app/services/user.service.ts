import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom, Observable } from 'rxjs';
import { SchoolSubject } from '../common/school-subject';
import { Grade } from '../common/grade';
import { ScheduleEvent } from '../common/schedule-event';
import { Student } from '../common/student';
import { Teacher } from '../common/teacher';
import { Parent } from '../common/parent';
import { StudentGroup } from '../common/student-group';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private mainUrl2 = 'http://127.0.0.1:8000';
  private mainUrl = 'http://localhost:8000';
  private options = {withCredentials: true, 'access-control-allow-origin': "http://localhost:4200/"};
  private userUrl = this.mainUrl + '/user';
  private currentUserId = localStorage.getItem('currentUserId');

  constructor(private http: HttpClient) {
  }

  async getAllGroups(): Promise<StudentGroup[]> {
    const url = `${this.mainUrl}/student-groups`;
    try {
      const response: getStudentGroupResponse[] = await lastValueFrom(this.http.get<getStudentGroupResponse[]>(url, { withCredentials: true }));
      return response.map(group => StudentGroup.fromApiResponse(group));
    } catch (error) {
      console.error('Błąd w ładowaniu groups:', error);
      return [];
    }
  }

  async getAllUserGroupIds(userId: number): Promise<number[]> {
    const url = `${this.userUrl}/${userId}/student/groups`;
    try {
      const response: getStudentGroupResponse[] = await lastValueFrom(this.http.get<getStudentGroupResponse[]>(url, { withCredentials: true }));
      return response.map(group => group.id);
    } catch (error) {
      console.error('Błąd w ładowaniu groups:', error);
      return [];
    }
  }
  
  async getAllUsersSubjects(userId: number): Promise<Map<number, Array<SchoolSubject>>> {
    const url = `${this.userUrl}/${userId}/student/groups`;
    const userGroups = await this.getAllUserGroupIds(userId);
    const subjects = new Map<number, Array<SchoolSubject>>();

    for (const groupId of userGroups) {
      try {
        const response = await lastValueFrom(this.http.get<getSubjectResponse[]>(`${url}/${groupId}/subjects`, { withCredentials: true }));
        const tempSubjects = response.map(element => SchoolSubject.fromApiResponse(element));
        subjects.set(groupId, tempSubjects);

      } catch (error) {
        console.error(`Błęd ładowania danych groupId ${groupId}:`, error);
      }
    }

    return subjects;
  }

  async getUsersGradesFromSubject(userId: number, subjectId: number): Promise<Array<Grade>> {
    const url = `${this.mainUrl}/grades/${userId}/${subjectId}`;
    try {
      const response = await lastValueFrom(this.http.get<getGradeResponse[]>(url, { withCredentials: true }));
      return response.map(element => Grade.fromApiResponse(element));

    } catch (error) {
      console.error('Błąd w ładowaniu ocen:', error);
      return [];
    }
  }

  async getUserSchedule(): Promise<Array<ScheduleEvent>> {
    const url = `${this.mainUrl}/meetings/schedule/`;
    try {
      const response = await lastValueFrom(this.http.get<getScheduleEventResponse[]>(url, { withCredentials: true }));
      return response.map(element => ScheduleEvent.fromApiResponse(element));

    } catch (error) {
      console.error('Błąd w ładowaniu rozkładu:', error);
      return [];
    }
  } 

  async getStudent(userId: number): Promise<Student | null> {
    const url = `${this.mainUrl}/students/${userId}`;
    try {
      const response = await lastValueFrom(this.http.get<getStudentResponse>(url, { withCredentials: true }));
      return Student.fromApiResponse(response);
    }
    catch (error) {
      console.error('Błąd w ładowaniu ucznia:', error);
      return null;
    } 
  }

  async getTeacher(userId: number): Promise<Teacher | null> {
    const url = `${this.mainUrl}/teachers/${userId}`;
    try {
      const response = await lastValueFrom(this.http.get<getTeacherResponse>(url, { withCredentials: true }));
      return Teacher.fromApiResponse(response);
    }
    catch (error) {
      console.error('Błąd w ładowaniu nauczyciela:', error);
      return null;
    } 
  }

  async getParent(userId: number): Promise<Parent | null> {
    const url = `${this.mainUrl}/parents/${userId}`;
    try {
      const response = await lastValueFrom(this.http.get<getParentResponse>(url, { withCredentials: true }));
      return Parent.fromApiResponse(response);
    }
    catch (error) {
      console.error('Błąd w ładowaniu rodzica:', error);
      return null;
    } 
  }

  getCurrentUserIdAsInt(): number {
    const storedUserId = localStorage.getItem('currentUserId');
    return storedUserId ? parseInt(storedUserId, 10) : -1;
  }

  getUserToken(): string {
    const storedUserToken = localStorage.getItem('xsrftoken')!;
    return storedUserToken;
  }

  getUserRole(): string {
    return localStorage.getItem('currentUserRole')!;
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

export interface getSubjectResponse {
  id: number;
  subject_name: string;
  description: string;
  is_mandatory: boolean;
  student_group: getStudentGroupResponse;
}

interface getStudentGroupResponse {
  id: number;
  name: string;
  description: string;
  level: number;
  section: string;
  students: number[];
}

export interface getGradeResponse {
  id: number;
  value: string;
  timestamp: string;
  student: number;
  grade_column: number;
  count_to_avg: boolean;
}

export interface getScheduleEventResponse {
  id: number;
  day_of_week: number;
  slot: number;
  teacher: getTeacherResponse;
  school_subject: getSubjectResponse;
  place: number;
}

interface getTeacherResponse {
  user_id: number;
  user: getUserResponse;
}

interface getParentResponse {
  userId: number;
  user: getUserResponse;
  children: number[];
}

interface getUserResponse {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  status: string;
  birth_date: string;
  sex: string;
  phone_number: string;
  photo_url: string;
  role: string;
}

interface getStudentResponse {
  user_id: number;
  user: getUserResponse;
  parents: number[];
}