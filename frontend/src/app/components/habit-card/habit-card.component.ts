import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Habit, Streak } from '../../models/interfaces';

@Component({
  selector: 'app-habit-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './habit-card.component.html',
  styleUrls: ['./habit-card.component.scss']
})
export class HabitCardComponent {
  @Input() habit!: Habit;
  @Input() streak?: Streak;
  @Input() animationDelay = 0;

  @Output() complete = new EventEmitter<number>();
  @Output() delete = new EventEmitter<number>();
  @Output() archive = new EventEmitter<number>();
  @Output() unarchive = new EventEmitter<number>();

  isCompleting = false;
  weekDays = [
    { label: 'L', name: 'Lunes', index: 0 },
    { label: 'M', name: 'Martes', index: 1 },
    { label: 'X', name: 'Miércoles', index: 2 },
    { label: 'J', name: 'Jueves', index: 3 },
    { label: 'V', name: 'Viernes', index: 4 },
    { label: 'S', name: 'Sábado', index: 5 },
    { label: 'D', name: 'Domingo', index: 6 },
  ];

  get currentStreak(): number {
    return this.streak?.current_streak || 0;
  }

  get longestStreak(): number {
    return this.streak?.longest_streak || 0;
  }

  get frequencyBadgeClass(): string {
    return `badge-${this.habit.frequency_type}`;
  }

  get frequencyLabel(): string {
    switch (this.habit.frequency_type) {
      case 'daily': return 'Diario';
      case 'weekly': return 'Semanal';
      case 'monthly': return 'Mensual';
      case 'custom': return 'Personalizado';
      default: return this.habit.frequency_type;
    }
  }

  get isTodayCompleted(): boolean {
    if (!this.streak?.last_completed_date) return false;
    const today = new Date().toISOString().split('T')[0];
    return this.streak.last_completed_date === today;
  }

  isDayTarget(dayIndex: number): boolean {
    if (this.habit.frequency_type === 'daily') return true;
    if (this.habit.frequency_type === 'custom' && this.habit.target_days) {
      return this.habit.target_days.includes(dayIndex);
    }
    return false;
  }

  onComplete(): void {
    if (this.isCompleting) return;
    this.isCompleting = true;
    this.complete.emit(this.habit.id);
    setTimeout(() => {
      this.isCompleting = false;
    }, 500);
  }

  onDelete(): void {
    this.delete.emit(this.habit.id);
  }


  onArchive(): void {
    this.archive.emit(this.habit.id);
  }

  onUnarchive(): void {
    this.unarchive.emit(this.habit.id);
  }
}
