import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { SchoolSubject } from '../../common/school-subject';
import { Student } from '../../common/student';
import { Grade } from '../../common/grade';

interface SubjectStatistics {
  subjectName: string;
  groupId: number;
  groupName: string;
  averageGrade: number;
  numberOfStudents: number;
  grades: {[key: number]: number}; // rozkład ocen
  totalGrades: number; // dodane: całkowita liczba ocen
}

interface StudentStatistics {
  subjectName: string;
  studentAverage: number;
  groupAverage: number;
  trend: number[]; // ostatnie 5 ocen
}

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.css']
})
export class StatisticsComponent implements OnInit {
  userRole: string = '';
  currentUserId: number;
  allSubjectsStats: Map<string, SubjectStatistics[]> = new Map();
  studentStats: StudentStatistics[] = [];
  isLoading: boolean = true;
  selectedSubject: string = '';
  
  constructor(private userService: UserService) {
    this.currentUserId = this.userService.getCurrentUserIdAsInt();
    this.userRole = this.userService.getUserRole();
  }

  async ngOnInit() {
    this.isLoading = true;
    await this.loadStatistics();
    this.isLoading = false;
  }

  private async loadStatistics() {
    if (this.userRole === 'student') {
      await this.loadStudentStatistics();
    } 
    await this.loadGroupStatistics();
  }

  private async loadStudentStatistics() {
    const subjects = await this.userService.getAllUsersSubjects(this.currentUserId);
    
    for (const [groupId, subjectsArray] of subjects.entries()) {
      for (const subject of subjectsArray) {
        const grades = await this.userService.getUsersGradesFromSubject(this.currentUserId, subject.id);
        const studentAvg = this.calculateAverage(grades.map(g => this.userService.parseGradeValue(g.value)));
        
        // Pobierz średnią grupy
        const groupStats = await this.calculateGroupStatistics(subject, groupId);
        
        this.studentStats.push({
          subjectName: subject.subjectName,
          studentAverage: studentAvg,
          groupAverage: groupStats.averageGrade,
          trend: this.getLastGrades(grades, 5)
        });
      }
    }
  }

  private async loadGroupStatistics() {
    const groups = await this.userService.getAllGroups();
    
    for (const group of groups) {
      const groupStudents = group.students;
      if (groupStudents && groupStudents.length > 0) {
        const firstStudent = groupStudents[0];
        const subjects = await this.userService.getAllUsersSubjects(firstStudent);
        
        for (const [groupId, subjectsArray] of subjects.entries()) {
          for (const subject of subjectsArray) {
            const stats = await this.calculateGroupStatistics(subject, groupId);
            
            if (!this.allSubjectsStats.has(subject.subjectName)) {
              this.allSubjectsStats.set(subject.subjectName, []);
            }
            
            const existingStats = this.allSubjectsStats.get(subject.subjectName);
            if (existingStats && !existingStats.find(s => s.groupId === groupId)) {
              existingStats.push(stats);
            }
          }
        }
      }
    }
  }

  private async calculateGroupStatistics(subject: SchoolSubject, groupId: number): Promise<SubjectStatistics> {
    const allGrades: number[] = [];
    const gradeDistribution: {[key: number]: number} = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0};
    let totalGrades = 0;
    
    const students = subject.studentGroup.students;
    for (const studentId of students) {
      const grades = await this.userService.getUsersGradesFromSubject(studentId, subject.id);
      grades.forEach(grade => {
        const value = this.userService.parseGradeValue(grade.value);
        if (value > 0) { // pomijamy nieprawidłowe oceny
          allGrades.push(value);
          gradeDistribution[value]++;
          totalGrades++;
        }
      });
    }

    return {
      subjectName: subject.subjectName,
      groupId: groupId,
      groupName: subject.studentGroup.name,
      averageGrade: this.calculateAverage(allGrades),
      numberOfStudents: students.length,
      grades: gradeDistribution,
      totalGrades: totalGrades
    };
  }

  private calculateAverage(grades: number[]): number {
    if (grades.length === 0) return 0;
    return Number((grades.reduce((a, b) => a + b, 0) / grades.length).toFixed(2));
  }

  private getLastGrades(grades: Grade[], count: number): number[] {
    return grades
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      .slice(0, count)
      .map(g => this.userService.parseGradeValue(g.value));
  }

  getSubjectsList(): string[] {
    return Array.from(this.allSubjectsStats.keys());
  }

  selectSubject(subject: string) {
    this.selectedSubject = subject;
    
    const statsSection = document.querySelector('.anim-display') as HTMLElement;
    if (statsSection) {
      // statsSection.classList.remove('slide-in-up');
      // void statsSection.offsetWidth;                     ewentualnie do zmiany potem
      // statsSection.classList.add('slide-in-up');
    }
  }

  getSelectedSubjectStats(): SubjectStatistics[] {
    return this.allSubjectsStats.get(this.selectedSubject) || [];
  }

  getFirstGroupStats(): SubjectStatistics | null {
    const stats = this.getSelectedSubjectStats();
    return stats.length > 0 ? stats[0] : null;
  }

  getGradeDistribution(stats: SubjectStatistics): {[key: number]: number} {
    return stats.grades;
  }

  calculateGradePercentage(stats: SubjectStatistics, count: number): number {
    if (!stats || stats.totalGrades === 0) return 0;
    const percentage = (count / stats.totalGrades) * 100;
    // Upewniamy się, że wartość nie jest NaN
    return isNaN(percentage) ? 0 : percentage;
  }

  getStudentStatsForSubject(subjectName: string): StudentStatistics | undefined {
    return this.studentStats.find(s => s.subjectName === subjectName);
  }
}