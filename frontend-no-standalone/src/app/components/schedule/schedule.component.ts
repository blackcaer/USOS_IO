import { Component } from '@angular/core';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrl: './schedule.component.css'
})
export class ScheduleComponent {
  constructor(private userService: UserService) {
  }

  hours = [
    "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"
  ];

  events = [
    {
      title: "Język angielski",
      time: "8:00 - 8:45",
      start: "8:00",
      end: "8:45",
      top: "0px",
      height: "45px",
      place: 1,
      day_of_week: 1
    },
    {
      title: "Matematyka",
      time: "8:50 - 9:35",
      start: "8:50",
      end: "9:35",
      top: "50px",
      height: "45px",
      place: 1,
      day_of_week: 1
    },
    {
      title: "Wychowanie fizyczne",
      time: "9:40 - 10:25",
      start: "9:40",
      end: "10:25",
      top: "100px",
      height: "45px",
      place: 1,
      day_of_week: 1
    },
    {
      title: "Biologia",
      time: "10:45 - 11:30",
      start: "10:45",
      end: "11:30",
      top: "225px",
      height: "45px",
      place: 1,
      day_of_week: 1
    },
    {
      title: "Historia",
      time: "13:25 - 14:10",
      start: "13:25",
      end: "14:10",
      top: "305px",
      height: "45px",
      place: 1,
      day_of_week: 1
    }
  ];

  weekEvents: { [key: number]: any[] } = {};

  async ngOnInit() {
    await this.fillEvents();
    console.log(this.events);
  } 


  async fillEvents() {
    try {
      const schedule = await this.userService.getUserSchedule();
      const scheduleSlots = [
        { slot: 1, start: "08:00", end: "08:45", top: "5px", height: "50px" },
        { slot: 2, start: "08:55", end: "09:40", top: "60px", height: "50px" },
        { slot: 3, start: "09:50", end: "10:35", top: "115px", height: "50px" },
        { slot: 4, start: "10:45", end: "11:30", top: "170px", height: "50px" },
        { slot: 5, start: "11:40", end: "12:25", top: "225px", height: "50px" },
        { slot: 6, start: "12:45", end: "13:30", top: "280px", height: "50px" },
        { slot: 7, start: "13:40", end: "14:25", top: "335px", height: "50px" },
        { slot: 8, start: "14:35", end: "15:20", top: "390px", height: "50px" },
      ];
  
      // Создаем сетку для событий
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

  /* async fillEvents() {
    try {
      const schedule = await this.userService.getUserSchedule();
      const scheduleSlots = [
        { slot: 1, start: "08:00", end: "08:45", top: "0px", height: "45px" },
        { slot: 2, start: "08:55", end: "09:40", top: "50px", height: "45px" },
        { slot: 3, start: "09:50", end: "10:35", top: "100px", height: "45px" },
        { slot: 4, start: "10:45", end: "11:30", top: "150px", height: "45px" },
        { slot: 5, start: "11:40", end: "12:25", top: "200px", height: "45px" },
        { slot: 6, start: "12:45", end: "13:30", top: "250px", height: "45px" },
        { slot: 7, start: "13:40", end: "14:25", top: "300px", height: "45px" },
        { slot: 8, start: "14:35", end: "15:20", top: "350px", height: "45px" },
      ];
  
      this.events = schedule.map((event) => {
        const slotInfo = scheduleSlots.find((slot) => slot.slot === event.slot);
  
        if (slotInfo) {
  
          return {
            title: event.school_subject.subjectName,
            time: `${slotInfo.start} - ${slotInfo.end}`,
            start: slotInfo.start,
            end: slotInfo.end,
            top: slotInfo.top,
            height: slotInfo.height,
            day_of_week: event.dayOfWeek,
            place: event.place
          };
        }
  
        return {
          title: "No Event",
          time: "",
          start: "",
          end: "",
          top: "0px",
          height: "0px",
          day_of_week: 1,
          place: 1
        };
      });
  
    } catch (error) {
      console.error("Błąd przy ładowaniu planu zajęć", error);
    }
  } */
}
