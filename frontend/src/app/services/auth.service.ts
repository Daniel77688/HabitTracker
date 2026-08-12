import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User, LoginRequest, RegisterRequest } from '../models/interfaces';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;

  constructor(private http: HttpClient) {}

  register(data: RegisterRequest): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/register`, data);
  }

  login(data: LoginRequest): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/login`, data);
  }

  getCurrentUser(): User | null {
    const stored = localStorage.getItem('habittracker_user');
    return stored ? JSON.parse(stored) : null;
  }

  saveUser(user: User): void {
    localStorage.setItem('habittracker_user', JSON.stringify(user));
  }

  logout(): void {
    localStorage.removeItem('habittracker_user');
  }

  isLoggedIn(): boolean {
    return !!this.getCurrentUser();
  }
}
