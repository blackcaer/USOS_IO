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
              private meetingService: MeetingService
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

  async ngOnInit() {
    await this.fillEvents();
    this.userRole = this.userService.getUserRole();
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
    return {
      title: "",
      description: "",
      start_time: "",
      teacher: 1,
      school_subject: 1
    }
  }

  openInfo(event: any) {
    this.infoEvent = event;
    console.log(this.infoEvent);
    this.isInfoOpen = true;

    if (this.userService.getUserRole() === 'teacher') {
      this.fillSubjectStudentList(event);
      console.log(this.subjectStudentList);
      this.fillMeetingData(event);
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
