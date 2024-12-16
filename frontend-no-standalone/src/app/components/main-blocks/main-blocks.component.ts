import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-main-blocks',
  templateUrl: './main-blocks.component.html',
  styleUrl: './main-blocks.component.css'
})
export class MainBlocksComponent {

private currentUserId: number;


constructor(private http: HttpClient,
            private userService: UserService
) {
  const storedUserId = localStorage.getItem('currentUserId');
  this.currentUserId = storedUserId ? parseInt(storedUserId, 10) : 0;
}

ngOnInit() {
  console.log(this.userService.getAllUsersSubjects(this.currentUserId));
}


  lastGrades = [
    { name: 'Matematyka', grade: -2 },
    { name: 'Informatyka', grade: 4 },
    { name: 'Angielski', grade: 4 },
    { name: 'Matematyka', grade: 1 },
    { name: 'Chemia', grade: 2 }
  ];
}


