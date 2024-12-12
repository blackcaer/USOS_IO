import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import {HttpClientXsrfModule} from '@angular/common/http';

import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { StatisticsComponent } from './components/statistics/statistics.component';
import { GradesComponent } from './components/grades/grades.component';
import { ScheduleComponent } from './components/schedule/schedule.component';
import { MainBlocksComponent } from './components/main-blocks/main-blocks.component';
import { RouterModule, Routes } from '@angular/router';


const routes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: 'statistics', component: StatisticsComponent},
  {path: 'grades', component: GradesComponent},
  {path: 'schedule', component: ScheduleComponent},
  {path: 'main', component: MainBlocksComponent},
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
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
