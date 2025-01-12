import { ConsentService } from './../../services/consent.service';
import { Component } from '@angular/core';
import { UserService } from '../../services/user.service';
import { Consent } from '../../common/consent';
import { ConsentTemplate } from '../../common/consent-template';
import { Parent } from '../../common/parent';
import { StudentGroup } from '../../common/student-group';
import { Student } from '../../common/student';
import { Teacher } from '../../common/teacher';

@Component({
  selector: 'app-consents',
  templateUrl: './consents.component.html',
  styleUrl: './consents.component.css'
})
export class ConsentsComponent {
  constructor(private userService: UserService,
              private consentService: ConsentService
    ) {
    }
  
  userRole = this.userService.getUserRole();
  userId = this.userService.getCurrentUserIdAsInt();

  pendingConsents: Consent[] = [];
  parentChildren: number[] = [];

  consentTemplates: ConsentTemplate[] = [];

  infoConsent: Consent | null = null;
  infoConsentTemplate: ConsentTemplate | null = null;
  infoParents: Parent[] = [];
  isInfoOpen = false;

  isCreateModalOpen = false;
  newConsent = {
    title: '',
    description: '',
    endDate: '',
    students: ''
  };
  selectedGroup: number = 0;
  groups: StudentGroup[] = [];
  groupStudents: Student[] = [];
  selectedStudents: Student[] = [];

  selectedFile: File | null = null;

  ngOnInit() {

    console.log(this.userRole);

    if (this.userRole === "parent") {
      this.fillPendingConsents();
      this.fillParentChildren();
    }
    if (this.userRole === "teacher") {
      this.fillConsentTemplates();
    }

  }

  fillParents() {
    if (!this.infoConsentTemplate) {
      console.error('ConsentTemplate nie jest wybrany.');
      return;
    }
  
    const parentConsentDetails = this.infoConsentTemplate.parentConsents;
  
    this.infoParents = [];
  
    parentConsentDetails.forEach((consent) => {
      this.userService.getParent(consent.parentUser).then((parent) => {
        if (parent) {
          this.infoParents.push(parent);
        }
      }).catch((error) => {
        console.error(`Błąd przy ładowaniu rodziców:`, error);
      });
    });
  }
  
  fillPendingConsents() {
    this.consentService.getPendingConsents()
      .then((consents) => {
        this.pendingConsents = consents;
        console.log(this.pendingConsents);
      })
      .catch((error) => {
        console.error('Błąd przy ładowaniu zgód:', error);
      });
  }

  fillParentChildren() {
    this.userService.getParent(this.userId)
      .then((parent) => {
        this.parentChildren = parent!.children;
      })
      .catch((error) => {
        console.error('Błąd przy ładowaniu dzieci rodzica:', error);
      });
  }

  fillConsentTemplates() {
    this.consentService.getConsentTemplates()
      .then((consents) => {
        this.consentTemplates = consents;
      })
      .catch((error) => {
        console.error('Błąd przy ładowaniu zgód:', error);
      });
  }

  fillGroups() {
    this.userService.getAllGroups()
    .then((groups) => {
      this.groups = groups;
    })
    .catch((error) => {
      console.error('Błąd przy ładowaniu grup:', error);
    });
  }

  fillSelectedGroupStudents() {
    const tempGroup = this.groups.find((group) => group.id === Number(this.selectedGroup));
  
    if (!tempGroup) {
      console.error('Nie znaleziono grupy o ID:', this.selectedGroup);
      return;
    }
  
    const groupStudentsId: number[] = tempGroup.students;
  
    for (const studentId of groupStudentsId) {
      this.userService.getStudent(studentId)
        .then((student) => {
          if (student) {
            this.groupStudents.push(student);
          } else {
            console.warn(`Nie znaleziono studenta o ID: ${studentId}`);
          }
        })
        .catch((error) => {
          console.error('Błąd przy ładowaniu studentów:', error);
        });
    }
  }

  getParentById(parentId: number): Parent | null {
    const parent = this.infoParents.find(p => p.userId === parentId);
    return parent || null;
  }

  viewFile(fileUrl: string): void {
    window.open(`http://localhost:8000${fileUrl}`, '_blank');
  }

  openInfoParent(consent: Consent) {
    this.infoConsent = consent;
    this.isInfoOpen = true;
  }

  openInfoTeacher(consent: ConsentTemplate) {
    this.infoConsentTemplate = consent;
    this.isInfoOpen = true;
    this.fillParents();
  }

  closeInfo() {
    this.infoConsent = null;
    this.infoConsentTemplate = null;
    this.isInfoOpen = false;
    this.infoParents = [];
    if (this.userRole === 'teacher') {
      this.fillConsentTemplates();
    } else if (this.userRole === 'parent') {
      this.fillPendingConsents();
    }
  }

  openCreateModal() {
    this.isCreateModalOpen = true;
    this.newConsent = {
      title: '',
      description: '',
      endDate: '',
      students: ''
    };
    this.selectedGroup = 0;
    this.groups = [];
    this.groupStudents = [];
    this.fillGroups();
  }

  onGroupChange() {
    this.groupStudents = [];
    this.selectedStudents = [];
    this.fillSelectedGroupStudents();
  }

  onStudentSelect(student: Student, event: any): void {
    if (event.target.checked) {
      this.selectedStudents.push(student);
    } else {
      this.selectedStudents = this.selectedStudents.filter(s => s !== student);
    }
    console.log(this.selectedStudents);
  }

  closeCreateModal() {
    this.isCreateModalOpen = false;
    this.newConsent = {
      title: '',
      description: '',
      endDate: '',
      students: ''
    };
    this.selectedGroup = 0;
    this.groups = [];
    this.groupStudents = [];
    if (this.userRole === "teacher") {
      this.fillConsentTemplates();
    }
  }

  createConsent() {
    let currentTeacher: Teacher | null = null;   
    
    this.userService.getTeacher(this.userId)
    .then((teacher) => {
      currentTeacher = teacher;
      
    })
    .catch((error) => {
      console.error('Błąd przy ładowaniu nauczyciela:', error);
    });

    let formData = {
      author: currentTeacher,
      title: this.newConsent.title,
      description: this.newConsent.description,
      end_date: this.newConsent.endDate,
      students: this.selectedStudents.map((student) => student.userId)
    }

    this.consentService.postConsentTemplate(formData).subscribe((consent) => {
      this.consentTemplates.push(ConsentTemplate.fromApiResponse(consent));
    })

    this.closeCreateModal();
  }

  deleteConsent(consentTemplateId: number) {
    this.consentService.deleteConsentTemplate(consentTemplateId);
    this.consentTemplates = this.consentTemplates.filter(template => template.id !== consentTemplateId);
    
    this.fillConsentTemplates();
    this.closeInfo();
  }

  formatDate(date: Date): string {  
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    
    const formattedDay = day < 10 ? `0${day}` : day;
    const formattedMonth = month < 10 ? `0${month}` : month;
    
    return `${formattedDay}.${formattedMonth}.${year}`;
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      console.log('File:', this.selectedFile);
    }
  }

  uploadFile(consent: boolean): void {
    if (!this.selectedFile) {
      alert('Należy najpierw wybrać plik!');
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);
    formData.append('is_consent', `${consent}`);
    formData.append('parent_user', `${this.userId}`);
    formData.append('child_user', `${this.parentChildren[0]}`);
    
    this.consentService.postParentConsent(this.infoConsent!.id, formData);   
    this.closeInfo(); 
  }
  
}

