import { Component } from '@angular/core';
import { UserService } from '../../services/user.service';
import { ScheduleEvent } from '../../common/schedule-event';
import { Student } from '../../common/student';
import { MeetingService } from '../../services/meeting.service';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrl: './schedule.component.css'
})
export class ScheduleComponent {
  constructor(private userService: UserService,
              private meetingService: MeetingService,
  ) {
  }

  hours = [
    "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"
  ];
  weekEvents: { [key: number]: any[] } = {};
  userRole: string = "";

  isInfoOpen: boolean = false;
  infoEvent: any = null;
  subjectStudentList: Array<Student> = [];

  currentData = new Date();
  firstCurrentWeekDay = this.getStartOfWeek(this.currentData);
  lastCurrentWeekDay = this.addDays(this.firstCurrentWeekDay, 6);

  async ngOnInit() {
    await this.fillEvents();
    this.userRole = this.userService.getUserRole();
  } 

  getActualWeek() {
    this.currentData = new Date();
    this.firstCurrentWeekDay = this.getStartOfWeek(this.currentData);
    this.lastCurrentWeekDay = this.addDays(this.firstCurrentWeekDay, 6);
  }

  getFollowingWeek() {
    this.currentData = new Date();
    this.firstCurrentWeekDay = this.addDays(this.getStartOfWeek(this.currentData), 7);
    this.lastCurrentWeekDay = this.addDays(this.firstCurrentWeekDay, 6);
  }

  getStartOfWeek(date: Date, startDay: number = 1): Date {
    // startDay: 0 = Niedziela, 1 = Poniedziałek
    const currentDay = date.getDay();
    const diff = (currentDay < startDay ? currentDay + 7 : currentDay) - startDay;
    const startOfWeek = new Date(date);
    startOfWeek.setDate(date.getDate() - diff);
    startOfWeek.setHours(0, 0, 0, 0);
    return startOfWeek;
  }

  addDays(date: Date, days: number): Date {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }

  startMeeting(event: any): void {
    const meetingData = this.getPostMeetingData(event);

    this.meetingService.createMeeting(meetingData).subscribe({
      next: (response) => {
        console.log('Meeting created successfully:', response);
      },
      error: (error) => {
        console.error('Error creating meeting:', error);
      },
    });
  }

  getPostMeetingData(event: any): any {
    const timeString = event.start;
    const [hours, minutes] = timeString.split(":").map(Number);

    return {
      title: event.eventInfo.school_subject.subjectName,
      description: event.eventInfo.school_subject.description,
      start_time: new Date(this.addDays(this.firstCurrentWeekDay, event.eventInfo.dayOfWeek - 1).setHours(hours + 1, minutes)),
      teacher: event.eventInfo.teacher.userId,
      school_subject: event.eventInfo.school_subject.id
    }
  }

  openInfo(event: any) {
    this.infoEvent = event;
    console.log(this.infoEvent);
    this.isInfoOpen = true;

    if (this.userService.getUserRole() === 'teacher') {
      this.fillSubjectStudentList(event);
      console.log(this.subjectStudentList);
      this.getPostMeetingData(event);
    }
  }

  fillSubjectStudentList(event: any) {
    for (let tempStudentId of event.eventInfo.school_subject.studentGroup.students) {
      const tempStudent = this.userService.getStudent(tempStudentId);
      tempStudent.then( student => {
        if (!!student) {
          this.subjectStudentList.push(student);
        }
      });
      
    }
  }

  closeInfo() {
    this.isInfoOpen = false;
    this.subjectStudentList = [];
  }

  async fillEvents() {
    try {
      const schedule = await this.userService.getUserSchedule();
      console.log(schedule);
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
  
      this.weekEvents = { 1: [], 2: [], 3: [], 4: [], 5: [] };
  
      schedule.forEach((event) => {
        const slotInfo = scheduleSlots.find((slot) => slot.slot === event.slot);
  
        if (slotInfo) {
          this.weekEvents[event.dayOfWeek].push({
            eventInfo: event,
            time: `${slotInfo.start} - ${slotInfo.end}`,
            start: slotInfo.start,
            end: slotInfo.end,
            top: slotInfo.top,
            height: slotInfo.height
          });
        }
      });
    } catch (error) {
      console.error("Błąd przy ładowaniu planu zajęć", error);
    }
  }
}
