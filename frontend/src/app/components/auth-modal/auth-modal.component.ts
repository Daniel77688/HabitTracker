import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/interfaces';

@Component({
  selector: 'app-auth-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './auth-modal.component.html',
  styleUrls: ['./auth-modal.component.scss']
})
export class AuthModalComponent {
  @Output() close = new EventEmitter<void>();
  @Output() authenticated = new EventEmitter<User>();

  activeTab: 'login' | 'register' = 'login';
  isLoading = false;
  error = '';

  loginForm = { username_or_email: '', password: '' };
  registerForm = { username: '', email: '', password: '' };

  constructor(private authService: AuthService) {}

  onLogin(): void {
    if (!this.loginForm.username_or_email || !this.loginForm.password) {
      this.error = 'Rellena todos los campos';
      return;
    }
    this.isLoading = true;
    this.error = '';
    this.authService.login(this.loginForm).subscribe({
      next: (user) => {
        this.authService.saveUser(user);
        this.authenticated.emit(user);
        this.isLoading = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Error al iniciar sesión';
        this.isLoading = false;
      }
    });
  }

  onRegister(): void {
    if (!this.registerForm.username || !this.registerForm.email || !this.registerForm.password) {
      this.error = 'Rellena todos los campos';
      return;
    }
    this.isLoading = true;
    this.error = '';
    this.authService.register(this.registerForm).subscribe({
      next: (user) => {
        this.authService.saveUser(user);
        this.authenticated.emit(user);
        this.isLoading = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Error al registrarse';
        this.isLoading = false;
      }
    });
  }

  onClose(): void {
    this.close.emit();
  }
}
