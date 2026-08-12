import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Habit, HabitCreate, HabitUpdate } from '../models/interfaces';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class HabitService {
  private apiUrl = `${environment.apiUrl}/habits`;

  constructor(private http: HttpClient) {}

  getHabitsByUser(userId: number): Observable<Habit[]> {
    return this.http.get<Habit[]>(`${this.apiUrl}/user/${userId}`);
  }

  getHabit(habitId: number): Observable<Habit> {
    return this.http.get<Habit>(`${this.apiUrl}/${habitId}`);
  }

  createHabit(data: HabitCreate): Observable<Habit> {
    return this.http.post<Habit>(this.apiUrl + '/', data);
  }

  updateHabit(habitId: number, data: HabitUpdate): Observable<Habit> {
    return this.http.put<Habit>(`${this.apiUrl}/${habitId}`, data);
  }

  deleteHabit(habitId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${habitId}`);
  }
}
