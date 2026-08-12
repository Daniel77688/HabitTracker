import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Streak } from '../models/interfaces';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class StreakService {
  private apiUrl = `${environment.apiUrl}/streaks`;

  constructor(private http: HttpClient) {}

  getStreakByHabit(habitId: number): Observable<Streak> {
    return this.http.get<Streak>(`${this.apiUrl}/habit/${habitId}`);
  }
}
