import { ConsentService } from './../../services/consent.service';
import { Component } from '@angular/core';
import { UserService } from '../../services/user.service';
import { Consent } from '../../common/consent';

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
  teacherNames: { [key: number]: string } = {};
  pendingConsents: Consent[] = [];
  parentChildren: number[] = [];

  infoConsent: Consent | null = null;
  isInfoOpen = false;

  selectedFile: File | null = null;

  ngOnInit() {
    this.fillPendingConsents();
    this.fillParentChildren();
    console.log(this.pendingConsents);
  }
  
  fillPendingConsents() {
    this.consentService.getPendingConsents()
      .then((consents) => {
        this.pendingConsents = consents;
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

/*   fillConsentTemplates() {
    this.consentService.getPendingConsents()
      .then((consents) => {
        this.pendingConsents = consents;
      })
      .catch((error) => {
        console.error('Błąd przy ładowaniu zgód:', error);
      });
  } */

  openInfo(consent: Consent) {
    this.infoConsent = consent;
    console.log(consent);
    this.isInfoOpen = true;
  }

  closeInfo() {
    this.infoConsent = null;
    this.isInfoOpen = false;
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

  uploadFile(): void {
    if (!this.selectedFile) {
      alert('Należy najpierw wybrać plik!');
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);
    formData.append('is_consent', 'true');
    formData.append('parent_user', `${this.userId}`);
    formData.append('child_user', `${this.parentChildren[0]}`);
    
    this.consentService.postParentConsent(this.infoConsent!.id, formData);    
  }






  
}

