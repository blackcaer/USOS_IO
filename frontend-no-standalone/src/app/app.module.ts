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
import { authGuard } from './guards/auth.guard';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { ConsentsComponent } from './components/consents/consents.component';


const routes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: 'statistics', component: StatisticsComponent, canActivate: [authGuard]},
  {path: 'grades', component: GradesComponent, canActivate: [authGuard]},
  {path: 'schedule', component: ScheduleComponent, canActivate: [authGuard]},
  {path: 'consents', component: ConsentsComponent, canActivate: [authGuard]},
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
    MainBlocksComponent,
    ConsentsComponent
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
  providers: [
    provideAnimationsAsync()
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
