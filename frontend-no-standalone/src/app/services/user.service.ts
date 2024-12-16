import { Injectable } from '@angular/core';
import { User } from '../common/user';
import { HttpBackend, HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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

    getAllUserGroups(userId: number): number[] {
      const url = `${this.userUrl}/${userId}/student/groups`;
      let groups: number[] = [];
    
      this.http.get<getResponseStudentGroup[]>(url, { withCredentials: true }).subscribe( response => {
        response.forEach( element => groups.push(element.id));
      });

      return groups;
    }
    
    getAllUsersSubjects(userId: number): Map<number, number[]> {
      const url = '${this.userUrl}/${userId}/student/groups';
      const userGroups: number[] = this.getAllUserGroups(userId);
      const subjects = new Map<number, number[]>();
      
      for (var groupId of userGroups) {
        this.http.get<getResponseSubject[]>(url + '/${groupId}/subjects', { withCredentials: true }).subscribe( response => {
          const tempSubjects: number[] = [];
          for (var element of response) {
            tempSubjects.push(element.id);
          }
          subjects.set(groupId, tempSubjects);
        });
      }

      return subjects;
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