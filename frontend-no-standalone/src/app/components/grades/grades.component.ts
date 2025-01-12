import { Component } from '@angular/core';
import { UserService } from '../../services/user.service';
import { Parent } from '../../common/parent';
import { Student } from '../../common/student';

@Component({
  selector: 'app-grades',
  templateUrl: './grades.component.html',
  styleUrl: './grades.component.css'
})
export class GradesComponent {

  currentUserId: number = this.userService.getCurrentUserIdAsInt();
  userRole = this.userService.getUserRole();
  student: Student | null = null;
  subjects = [
    { name: 'Biologia', grades: [4, 3, 2, 5] },
    { name: 'Matematyka', grades: [3, 1, 2] },
    { name: 'Informatyka', grades: [4, 3, 2, -5, 4] },
    { name: 'Historia', grades: [-5, 3] },
    { name: 'Wychowanie Fizyczne', grades: [-5, 4, 2, 4, 5] },
    { name: 'Angielski', grades: [-3, 3, 2, 4, 4] },
    { name: 'Chemia', grades: [2, 2, 2 ,2] }
  ];

  constructor(private userService: UserService) {
  }

  ngOnInit() {
    if (this.userRole === 'student') {
      this.fillAllSubjectsGrades(this.currentUserId);
      this.userService.getStudent(this.currentUserId)
        .then((student) => {
          this.student = student;
        })
        .catch((error) => {
          console.error('Błąd w ładowaniu studenta', error);
        });
    } else if (this.userRole === 'parent') {
      this.userService.getParent(this.currentUserId)
        .then((parent) => {
          if (parent?.children && parent.children.length > 0) {
            const childId = parent.children[0];
            
            this.fillAllSubjectsGrades(childId);
  
            this.userService.getStudent(childId)
              .then((student) => {
                this.student = student;
              })
              .catch((error) => {
                console.error('Błąd w ładowaniu studenta', error);
              });
          } else {
            console.error('Brak dzieci w danych rodzica');
          }
        })
        .catch((error) => {
          console.error('Błąd w ładowaniu rodzica', error);
        });
    }
  }
  

  async fillAllSubjectsGrades(userId: number) {
    this.subjects = [];
  
    try {
      const subjectsData = await this.userService.getAllUsersSubjects(userId);
  
      for (const [groupId, subjectsArray] of subjectsData.entries()) {
        for (const subject of subjectsArray) {
          try {
            const grades = await this.userService.getUsersGradesFromSubject(userId, subject.id);
  
            const numericGrades = grades.map(grade => this.userService.parseGradeValue(grade.value));
  
            const existingSubject = this.subjects.find(s => s.name === subject.subjectName);
            if (existingSubject) {
              existingSubject.grades = [...existingSubject.grades, ...numericGrades];
            } else {
              this.subjects.push({ name: subject.subjectName, grades: numericGrades });
            }
          } catch (error) {
            console.error(`Błąd w ładowaniu ocen dla przedmiotu ${subject.subjectName} (grupa ${groupId}):`, error);
          }
        }
      }
    } catch (error) {
      console.error('Błąd w ładowaniu przedmiotów:', error);
    }
  
    console.log(this.subjects);
  }

  
}
