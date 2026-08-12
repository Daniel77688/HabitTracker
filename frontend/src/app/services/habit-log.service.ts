import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HabitLog, HabitLogCreate } from '../models/interfaces';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class HabitLogService {
  private apiUrl = `${environment.apiUrl}/habit-logs`;

  constructor(private http: HttpClient) {}

  logCompletion(data: HabitLogCreate): Observable<HabitLog> {
    return this.http.post<HabitLog>(this.apiUrl + '/', data);
  }

  getLogsByHabit(habitId: number): Observable<HabitLog[]> {
    return this.http.get<HabitLog[]>(`${this.apiUrl}/habit/${habitId}`);
  }

  deleteLog(logId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${logId}`);
  }
}
