import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import {HttpClientXsrfModule} from '@angular/common/http';
import { MatDialogModule } from '@angular/material/dialog';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatButtonModule } from '@angular/material/button';

import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { StatisticsComponent } from './components/statistics/statistics.component';
import { GradesComponent } from './components/grades/grades.component';
import { ScheduleComponent } from './components/schedule/schedule.component';
import { MainBlocksComponent } from './components/main-blocks/main-blocks.component';
import { RouterModule, Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';


const routes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: 'statistics', component: StatisticsComponent, canActivate: [authGuard]},
  {path: 'grades', component: GradesComponent, canActivate: [authGuard]},
  {path: 'schedule', component: ScheduleComponent, canActivate: [authGuard]},
  {path: 'main', component: MainBlocksComponent, canActivate: [authGuard]},
  {path: '', redirectTo: 'main', pathMatch: 'full'},
  {path: '**', redirectTo: 'main', pathMatch: 'full'}
];

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    StatisticsComponent,
    GradesComponent,
    ScheduleComponent,
    MainBlocksComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    ReactiveFormsModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken',
    }),
    MatDialogModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatButtonModule,
  ],
  providers: [
    provideAnimationsAsync()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
