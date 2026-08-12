import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { HabitService } from '../../services/habit.service';
import { HabitLogService } from '../../services/habit-log.service';
import { StreakService } from '../../services/streak.service';
import { User, Habit, Streak, FrequencyType } from '../../models/interfaces';
import { AuthModalComponent } from '../auth-modal/auth-modal.component';
import { HabitCardComponent } from '../habit-card/habit-card.component';
import { forkJoin } from 'rxjs';

import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, AuthModalComponent, HabitCardComponent],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  user: User | null = null;
  habits: Habit[] = [];
  streaks: Map<number, Streak> = new Map();
  showAuthModal = false;
  showCreateForm = false;
  isLoading = false;
  authAction = '';
  searchQuery = '';
  selectedFrequency: string = 'all';

  activeTab: 'active' | 'archived' = 'active';
  currentTheme: 'dark' | 'light' = 'dark';

  habitToDelete: Habit | null = null;
  showDeleteConfirmModal = false;



  newHabit = {
    title: '',
    description: '',
    frequency_type: 'daily' as FrequencyType,
    target_days: [] as number[]
  };

  dayLabels = [
    { label: 'Lun', index: 0 },
    { label: 'Mar', index: 1 },
    { label: 'Mié', index: 2 },
    { label: 'Jue', index: 3 },
    { label: 'Vie', index: 4 },
    { label: 'Sáb', index: 5 },
    { label: 'Dom', index: 6 },
  ];

  frequencyOptions: { value: FrequencyType; label: string; desc: string }[] = [
    { value: 'daily', label: 'Diario', desc: 'Cada día de la semana' },
    { value: 'weekly', label: 'Semanal', desc: 'Una vez a la semana' },
    { value: 'monthly', label: 'Mensual', desc: 'Una vez al mes' },
    { value: 'custom', label: 'Personalizado', desc: 'Días concretos' }
  ];

  constructor(
    private authService: AuthService,
    private habitService: HabitService,
    private habitLogService: HabitLogService,
    private streakService: StreakService
  ) {}

  ngOnInit(): void {
    this.initTheme();
    this.user = this.authService.getCurrentUser();
    if (this.user) {
      this.loadHabits();
    }
  }

  initTheme(): void {
    const saved = localStorage.getItem('habittracker_theme') as 'dark' | 'light';
    this.currentTheme = saved || 'dark';
    document.documentElement.setAttribute('data-theme', this.currentTheme);
  }

  toggleTheme(): void {
    this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', this.currentTheme);
    localStorage.setItem('habittracker_theme', this.currentTheme);
  }

  get filteredActiveHabits(): Habit[] {
    return this.habits.filter(h => {
      if (h.status !== 'active') return false;
      if (this.selectedFrequency !== 'all' && h.frequency_type !== this.selectedFrequency) return false;
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        return h.title.toLowerCase().includes(query) || (h.description && h.description.toLowerCase().includes(query));
      }
      return true;
    });
  }

  get filteredArchivedHabits(): Habit[] {
    return this.habits.filter(h => {
      if (h.status !== 'archived') return false;
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        return h.title.toLowerCase().includes(query);
      }
      return true;
    });
  }

  get totalActiveCount(): number {
    return this.habits.filter(h => h.status === 'active').length;
  }

  get totalArchivedCount(): number {
    return this.habits.filter(h => h.status === 'archived').length;
  }

  get totalStreaks(): number {
    let total = 0;
    this.streaks.forEach(s => total += s.current_streak);
    return total;
  }

  get bestStreak(): number {
    let best = 0;
    this.streaks.forEach(s => {
      if (s.longest_streak > best) best = s.longest_streak;
    });
    return best;
  }

  get completedTodayCount(): number {
    const today = new Date().toISOString().split('T')[0];
    let count = 0;
    this.streaks.forEach(s => {
      if (s.last_completed_date === today) count++;
    });
    return count;
  }

  requireAuth(action: string): void {
    if (!this.user) {
      this.authAction = action;
      this.showAuthModal = true;
    }
  }

  onAuthenticated(user: User): void {
    this.user = user;
    this.showAuthModal = false;
    this.loadHabits();
    if (this.authAction === 'create') {
      this.showCreateForm = true;
    }
    this.authAction = '';
  }

  logout(): void {
    this.authService.logout();
    this.user = null;
    this.habits = [];
    this.streaks.clear();
    this.showCreateForm = false;
  }

  loadHabits(): void {
    if (!this.user) return;
    this.isLoading = true;
    this.habitService.getHabitsByUser(this.user.id).subscribe({
      next: (habits) => {
        this.habits = habits;
        this.loadStreaks(habits);
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  loadStreaks(habits: Habit[]): void {
    if (habits.length === 0) return;
    const requests = habits.map(h => this.streakService.getStreakByHabit(h.id));
    forkJoin(requests).subscribe({
      next: (streaks) => {
        streaks.forEach(s => this.streaks.set(s.habit_id, s));
      }
    });
  }

  toggleDay(day: number): void {
    const idx = this.newHabit.target_days.indexOf(day);
    if (idx > -1) {
      this.newHabit.target_days.splice(idx, 1);
    } else {
      this.newHabit.target_days.push(day);
    }
  }

  createHabit(): void {
    if (!this.user || !this.newHabit.title.trim()) return;

    const payload: any = {
      user_id: this.user.id,
      title: this.newHabit.title.trim(),
      description: this.newHabit.description.trim() || undefined,
      frequency_type: this.newHabit.frequency_type,
    };

    if (this.newHabit.frequency_type === 'custom' && this.newHabit.target_days.length > 0) {
      payload.target_days = this.newHabit.target_days;
    }

    this.habitService.createHabit(payload).subscribe({
      next: (habit) => {
        this.habits.push(habit);
        this.resetForm();
      }
    });
  }

  onHabitCompleted(habitId: number): void {
    this.habitLogService.logCompletion({ habit_id: habitId }).subscribe({
      next: () => {
        this.streakService.getStreakByHabit(habitId).subscribe({
          next: (streak) => {
            this.streaks.set(habitId, streak);
          }
        });
      }
    });
  }

  onHabitDeleted(habitId: number): void {
    const habit = this.habits.find(h => h.id === habitId);
    if (habit) {
      this.habitToDelete = habit;
      this.showDeleteConfirmModal = true;
    }
  }

  confirmDeleteHabit(): void {
    if (!this.habitToDelete) return;
    const habitId = this.habitToDelete.id;
    this.habitService.deleteHabit(habitId).subscribe({
      next: () => {
        this.habits = this.habits.filter(h => h.id !== habitId);
        this.streaks.delete(habitId);
        this.cancelDeleteHabit();
      }
    });
  }

  cancelDeleteHabit(): void {
    this.habitToDelete = null;
    this.showDeleteConfirmModal = false;
  }


  onHabitArchived(habitId: number): void {
    this.habitService.updateHabit(habitId, { status: 'archived' }).subscribe({
      next: (updated) => {
        const idx = this.habits.findIndex(h => h.id === habitId);
        if (idx > -1) this.habits[idx] = updated;
      }
    });
  }

  onHabitUnarchived(habitId: number): void {
    this.habitService.updateHabit(habitId, { status: 'active' }).subscribe({
      next: (updated) => {
        const idx = this.habits.findIndex(h => h.id === habitId);
        if (idx > -1) this.habits[idx] = updated;
      }
    });
  }

  resetForm(): void {
    this.newHabit = { title: '', description: '', frequency_type: 'daily', target_days: [] };
    this.showCreateForm = false;
  }

  openCreate(): void {
    if (!this.user) {
      this.requireAuth('create');
      return;
    }
    this.showCreateForm = true;
  }
}
