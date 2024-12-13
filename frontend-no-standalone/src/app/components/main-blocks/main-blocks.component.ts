import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-main-blocks',
  templateUrl: './main-blocks.component.html',
  styleUrl: './main-blocks.component.css'
})
export class MainBlocksComponent {

private currentUserId: number;
lastGrades = [
  { name: 'Matematyka', grade: -2 },
  { name: 'Informatyka', grade: 4 },
  { name: 'Angielski', grade: 4 },
  { name: 'Matematyka', grade: 1 },
  { name: 'Chemia', grade: 2 }
];
hours = [
  "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"
];

constructor(private http: HttpClient,
            private userService: UserService
) {
  this.currentUserId = this.userService.getUserIdAsInt();

  this.events = this.events.map(event => ({
    ...event,
    ...this.calculateEventStyles(event)
  }));
}

  ngOnInit() {
    this.fillLastGrades();
  }

  async fillLastGrades() {
    this.lastGrades = [];
  
    try {
      const subjectsMap = await this.userService.getAllUsersSubjects(this.currentUserId);
      const allGrades: { name: string, grade: number, timestamp: Date }[] = [];
  
      for (const [groupId, subjects] of subjectsMap) {
        for (const subject of subjects) {
          const gradesWithTimestamps = await this.userService.getUsersGradesFromSubjectWithTimestamp(this.currentUserId, subject.id);
  
          gradesWithTimestamps.forEach(grade => {
            allGrades.push({
              name: subject.name,
              grade: this.userService.parseGradeValue(grade.value),
              timestamp: grade.timestamp
            });
          });
        }
      }
  
      const sortedGrades = allGrades.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());

      const lastFiveGrades = sortedGrades.slice(0, 5);
  
      this.lastGrades = lastFiveGrades;
  
      console.log('Ostatnie 5 ocen:', this.lastGrades);
    } catch (error) {
      console.error('Błąd podczas ładowania ostatnich ocen:', error);
    }
  }

  calculateEventStyles(event: any) {
    const timeToMinutes = (time: string): number => {
      const [hours, minutes] = time.split(":").map(Number);
      return hours * 60 + minutes;
    };
  
    const coef = 0.87;
    const startOfDay = timeToMinutes(this.hours[0]);
    const startMinutes = (timeToMinutes(event.start) - startOfDay);
    const endMinutes = (timeToMinutes(event.end) - startOfDay);
  
    const top = `${coef * startMinutes}px`;
    const height = `${0.94 * (endMinutes - startMinutes)}px`;
  
    return { top, height };
 
  }; 

  events = [
    {
      title: "Język angielski",
      time: "8:00 - 8:45",
      start: "8:00",
      end: "8:45",
      top: "0px",
      height: "45px"
    },
    {
      title: "Matematyka",
      time: "8:50 - 9:35",
      start: "8:50",
      end: "9:35",
      top: "50px",
      height: "45px"
    },
    {
      title: "Wychowanie fizyczne",
      time: "9:40 - 10:25",
      start: "9:40",
      end: "10:25",
      top: "100px",
      height: "45px"
    },
    {
      title: "Biologia",
      time: "10:45 - 11:30",
      start: "10:45",
      end: "11:30",
      top: "225px",
      height: "45px"
    },
    {
      title: "Historia",
      time: "13:25 - 14:10",
      start: "13:25",
      end: "14:10",
      top: "305px",
      height: "45px"
    }
  ];  
}


