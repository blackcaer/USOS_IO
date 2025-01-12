import { lastValueFrom } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-main-blocks',
  templateUrl: './main-blocks.component.html',
  styleUrl: './main-blocks.component.css'
})
export class MainBlocksComponent {

  currentUserId: number = this.userService.getCurrentUserIdAsInt();
  userRole = this.userService.getUserRole();
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
  weekEvents: { [key: number]: any[] } = {};
  currentDay: number = new Date().getDay() <= 5 && new Date().getDay() > 0 ? new Date().getDay() : 1;
  currentDayName: string = this.getDayName(this.currentDay);

  constructor(private http: HttpClient,
              private userService: UserService
  ) {

  }

  async ngOnInit() {
    if (this.userRole === 'student') {
      await this.fillLastGrades(this.currentUserId);
    } else if (this.userRole === 'parent') {
      this.userService.getParent(this.currentUserId)
        .then((parent) => {
          if (parent?.children && parent.children.length > 0) {
            const childId = parent.children[0];

            this.fillLastGrades(childId);
          }
        })
        .catch((error) => {
          console.error('Błąd w ładowaniu studenta', error);
        });
    }

    
    await this.fillEvents();
  }

  async fillLastGrades(userId: number) {
    this.lastGrades = [];
  
    try {
      const subjectsMap = await this.userService.getAllUsersSubjects(userId);
      const allGrades: { name: string, grade: number, date: Date }[] = [];
  
      for (const [groupId, subjects] of subjectsMap.entries()) {
        for (const subject of subjects) {
          try {
            const grades = await this.userService.getUsersGradesFromSubject(userId, subject.id);
  
            grades.forEach(grade => {
              allGrades.push({
                name: subject.subjectName,
                grade: this.userService.parseGradeValue(grade.value),
                date: grade.timestamp
              });
            });
          } catch (error) {
            console.error(`Błąd podczas ładowania ocen dla przedmiotu ${subject.subjectName} (grupa ${groupId}):`, error);
          }
        }
      }
  
      const sortedGrades = allGrades.sort((a, b) => b.date.getTime() - a.date.getTime());
  
      this.lastGrades = sortedGrades.slice(0, 5);
    } catch (error) {
      console.error('Błąd podczas ładowania ostatnich ocen:', error);
    } 
  }; 

  async fillEvents() {
    try {
      const schedule = await this.userService.getUserSchedule();
      const scheduleSlots = [
        { slot: 1, start: "08:00", end: "08:45", top: "4px", height: "42px" },
        { slot: 2, start: "08:55", end: "09:40", top: "50px", height: "42px" },
        { slot: 3, start: "09:50", end: "10:35", top: "96px", height: "42px" },
        { slot: 4, start: "10:45", end: "11:30", top: "142px", height: "42px" },
        { slot: 5, start: "11:40", end: "12:25", top: "188px", height: "42px" },
        { slot: 6, start: "12:45", end: "13:30", top: "134px", height: "42px" },
        { slot: 7, start: "13:40", end: "14:25", top: "180px", height: "42px" },
        { slot: 8, start: "14:35", end: "15:20", top: "226px", height: "42px" },
      ];
  
      this.weekEvents = { 1: [], 2: [], 3: [], 4: [], 5: [] };
  
      schedule.forEach((event) => {
        const slotInfo = scheduleSlots.find((slot) => slot.slot === event.slot);
  
        if (slotInfo) {
          this.weekEvents[event.dayOfWeek].push({
            title: event.school_subject.subjectName,
            time: `${slotInfo.start} - ${slotInfo.end}`,
            start: slotInfo.start,
            end: slotInfo.end,
            top: slotInfo.top,
            height: slotInfo.height,
            place: event.place,
          });
        }
      });
    } catch (error) {
      console.error("Błąd przy ładowaniu planu zajęć", error);
    }
  }

  // showNextDay() {
  //   this.currentDay = this.currentDay === 5 ? 5 : this.currentDay + 1;
  //   this.currentDayName = this.getDayName(this.currentDay);
  // }

  // showPreviousDay() {
  //   this.currentDay = this.currentDay === 1 ? 1 : this.currentDay - 1;
  //   this.currentDayName = this.getDayName(this.currentDay);
  // }

  // getDayName(day: number): string {
  //   const days = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek'];
  //   return days[day - 1];
  // }

  isSliding: boolean = false;

  showNextDay() {
    if (this.isSliding) return;
    this.isSliding = true;
  
    const content = document.querySelector('.schedule-content') as HTMLElement;
  
    // Faza chowania w lewo
    content.classList.add('slide-out-left');
    setTimeout(() => {
      content.classList.remove('slide-out-left');
  
      // Zmień aktualny dzień
      this.currentDay = this.currentDay === 5 ? 1 : this.currentDay + 1;
      this.currentDayName = this.getDayName(this.currentDay);
  
      // Faza wchodzenia z prawej
      content.classList.add('slide-in-right');
      setTimeout(() => {
        content.classList.remove('slide-in-right');
        this.isSliding = false;
      }, 300); // Czas trwania animacji
    }, 300); // Czas trwania animacji chowania
  }
  
  showPreviousDay() {
    if (this.isSliding) return;
    this.isSliding = true;
  
    const content = document.querySelector('.schedule-content') as HTMLElement;
  
    // Faza chowania w prawo
    content.classList.add('slide-out-right');
    setTimeout(() => {
      content.classList.remove('slide-out-right');
  
      // Zmień aktualny dzień
      this.currentDay = this.currentDay === 1 ? 5 : this.currentDay - 1;
      this.currentDayName = this.getDayName(this.currentDay);
  
      // Faza wchodzenia z lewej
      content.classList.add('slide-in-left');
      setTimeout(() => {
        content.classList.remove('slide-in-left');
        this.isSliding = false;
      }, 300); // Czas trwania animacji
    }, 300); // Czas trwania animacji chowania
  }
  

  getDayName(day: number): string {
    const days = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek'];
    return days[day - 1];
  }
}