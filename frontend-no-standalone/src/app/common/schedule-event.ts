import { SchoolSubject } from "./school-subject";
import { Teacher } from "./teacher";

export class ScheduleEvent {
    constructor(
      public id: number,
      public dayOfWeek: number,
      public slot: number,
      public teacher: Teacher,
      public school_subject: SchoolSubject,
      public place: number
    ) {}
  
    static fromApiResponse(response: any): ScheduleEvent {
      return new ScheduleEvent(
        response.id,
        response.day_of_week,
        response.slot,
        Teacher.fromApiResponse(response.teacher),
        SchoolSubject.fromApiResponse(response.school_subject),
        response.place
      );
    }
  }
