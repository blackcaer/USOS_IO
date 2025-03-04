import { Component } from '@angular/core';
import { UserService } from '../../services/user.service';
import { Student } from '../../common/student';
import { Teacher } from '../../common/teacher';
import { StudentGroup } from '../../common/student-group';
import { SchoolSubject } from '../../common/school-subject';
import { MeetingService } from '../../services/meeting.service';
import { GradeColumn } from '../../common/grade-column';
import { timestamp } from 'rxjs';

@Component({
  selector: 'app-grades',
  templateUrl: './grades.component.html',
  styleUrl: './grades.component.css'
})
export class GradesComponent {
  currentUserId: number = this.userService.getCurrentUserIdAsInt();
  userRole = this.userService.getUserRole();
  student: Student | null = null;
  teacher: Teacher | null = null;
  
  groups: StudentGroup[] = [];
  selectedGroup: StudentGroup | null = null;
  groupStudents: Student[] = [];
  selectedStudent: Student | null = null;
  teacherSubjects: SchoolSubject[] = [];
  gradeColumns: GradeColumn[] = [];
  selectedSubject: SchoolSubject | null = null;

  
  isGradeModalOpen = false;
  newGrade = {
    value: '',
    countToAvg: true,
    subject: null as number | null,
    gradeColumn: null as GradeColumn | null
  };
  
  subjects: { name: string; grades: number[] }[] = [];

  constructor(private userService: UserService,
              private meetingService: MeetingService
  ) {}

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
          }
        });
    } else if (this.userRole === 'teacher') {
      this.initTeacherData();
    }
  }

  async initTeacherData() {
    try {
      this.teacher = await this.userService.getTeacher(this.currentUserId);
      if (!this.teacher) return;

      this.groups = await this.userService.getAllGroups();
      
    } catch (error) {
      console.error('Błąd podczas inicjalizacji danych nauczyciela:', error);
    }
  }

  async onGroupSelect(group: StudentGroup) {
    this.selectedGroup = group;
    this.teacherSubjects = await this.meetingService.getTeachersSubjectsBySubstring(group.name);
    console.log(this.teacherSubjects);
    this.selectedStudent = null;
    this.subjects = [];
    
    try {
      const promises = group.students.map(studentId => 
        this.userService.getStudent(studentId)
      );
      
      this.groupStudents = (await Promise.all(promises)).filter((student): student is Student => 
        student !== null
      );
    } catch (error) {
      console.error('Błąd podczas ładowania studentów grupy:', error);
    }
  }

  async onStudentSelect(student: Student) {
    this.selectedStudent = student;
    await this.fillAllSubjectsGrades(student.userId);
  }

  openGradeModal() {
    if (!this.selectedStudent) return;
    
    this.selectedSubject = null;
    this.isGradeModalOpen = true;
    this.newGrade = {
      value: '',
      countToAvg: true,
      subject: null,
      gradeColumn: null
    };
  }

  onSubjectChange() {
    this.gradeColumns = [];
    this.meetingService.getSubjectsGradeColumns(this.selectedSubject!)
      .then((gradeColumns) => this.gradeColumns = gradeColumns);
  }

  closeGradeModal() {
    this.isGradeModalOpen = false;
    this.selectedSubject = null;
    if (this.selectedStudent) {
      this.fillAllSubjectsGrades(this.selectedStudent.userId);
    }
  }

  async addGrade() {
    if (!this.selectedStudent || !this.selectedSubject || !this.newGrade.value || !this.newGrade.gradeColumn) return;

    try {
      await this.meetingService.postGrade({
        value: this.newGrade.value,
        timestamp: new Date(),
        student: this.selectedStudent.userId,
        grade_column: this.newGrade.gradeColumn.id,
        countToAvg: this.newGrade.countToAvg
      }, this.selectedStudent.userId, this.selectedSubject!.id).subscribe(response => console.log(response));
      
      this.closeGradeModal();
    } catch (error) {
      alert("Ocena z tego tematu już jest dodana");
      console.error('Błąd podczas dodawania oceny:', error);
    }
  }

  async fillAllSubjectsGrades(userId: number) {
    this.subjects = [];
    try {
      const subjectsData = await this.userService.getAllUsersSubjects(userId);
      for (const [groupId, subjectsArray] of subjectsData.entries()) {
        for (const subject of subjectsArray) {
          const grades = await this.userService.getUsersGradesFromSubject(userId, subject.id);
          const numericGrades = grades.map(grade => this.userService.parseGradeValue(grade.value));
          
          const existingSubject = this.subjects.find(s => s.name === subject.subjectName);
          if (existingSubject) {
            existingSubject.grades = [...existingSubject.grades, ...numericGrades];
          } else {
            this.subjects.push({ name: subject.subjectName, grades: numericGrades });
          }
        }
      }
    } catch (error) {
      console.error('Błąd w ładowaniu przedmiotów:', error);
    }
  }
}