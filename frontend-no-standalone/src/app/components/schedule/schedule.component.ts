import { Component } from '@angular/core';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrl: './schedule.component.css'
})
export class ScheduleComponent {
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

  ngOnInit() {
    this.events = this.events.map(event => ({
      ...event,
      ...this.calculateEventStyles(event)
    }));
  }

  calculateEventStyles = (event: any) => {
    const timeToMinutes = (time: string): number => {
      const [hours, minutes] = time.split(":").map(Number);
      return hours * 60 + minutes;
    };
  
    const coef = 1.03;
    const startOfDay = timeToMinutes(this.hours[0]);
    const startMinutes = (timeToMinutes(event.start) - startOfDay);
    const endMinutes = coef * (timeToMinutes(event.end) - startOfDay);
  
    const top = `${startMinutes}px`;
    const height = `${endMinutes - startMinutes}px`;
  
    return { top, height };
 
  }; 


  
}
