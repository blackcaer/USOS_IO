import { Component } from '@angular/core';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-grades',
  templateUrl: './grades.component.html',
  styleUrl: './grades.component.css'
})
export class GradesComponent {

  private currentUserId: number;
  subjects = [
    { name: 'Biologia', grades: [-4, 3, -2, -5] },
    { name: 'Matematyka', grades: [3, 1, -2] },
    { name: 'Informatyka', grades: [-4, 3, -2, -5, 4] },
    { name: 'Historia', grades: [-5, 3] },
    { name: 'Wychowanie Fizyczne', grades: [-5, 4, 2, 4, 5] },
    { name: 'Angielski', grades: [-3, 3, 2, 4, 4] },
    { name: 'Chemia', grades: [2, 2, 2 ,2] }
  ];

  constructor(private userService: UserService) {
    this.currentUserId = this.userService.getUserIdAsInt();
  }

  ngOnInit() {
    this.fillAllSubjectsGrades()
  }

  async fillAllSubjectsGrades() {
    this.subjects = [];

    const subjectsData = await this.userService.getAllUsersSubjects(this.currentUserId);
  
    // Проходим по каждому предмету для пользователя
    for (const [groupId, subjectsArray] of subjectsData.entries()) {
      for (const subject of subjectsArray) {
        try {
          // Получаем все оценки для конкретного предмета
          const grades = await this.userService.getUsersGradesFromSubject(this.currentUserId, subject.id);
  
          // Преобразуем оценки с использованием метода parseGradeValue
          const numericGrades = grades.map(grade => this.userService.parseGradeValue(grade));
  
          // Если предмет уже существует в массиве subjects, добавляем оценки
          const existingSubject = this.subjects.find(s => s.name === subject.name);
          if (existingSubject) {
            existingSubject.grades = [...existingSubject.grades, ...numericGrades];
          } else {
            // Если предмет ещё не добавлен в массив, создаём новый
            this.subjects.push({ name: subject.name, grades: numericGrades });
          }
  
        } catch (error) {
          console.error('Ошибка при загрузке оценок для предмета', subject.name, error);
        }
      }
    }
  
    console.log(this.subjects); // Выводим массив с предметами и оценками
  }

  
}
