import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { HabitService } from '../../services/habit.service';
import { HabitLogService } from '../../services/habit-log.service';
import { User, Habit, HabitLog } from '../../models/interfaces';

type CalendarView = 'week' | 'month' | 'year' | 'custom';

interface DayHabitStatus {
  habit: Habit;
  completed: boolean;
}

interface CalendarDay {
  date: string;        // YYYY-MM-DD
  dateObj: Date;
  scheduledHabits: DayHabitStatus[];
  completedCount: number;
  totalScheduled: number;
  isToday: boolean;
  isCurrentMonth: boolean;
  isInRange: boolean;
}

interface WeekRow {
  weekLabel: string;
  days: CalendarDay[];
}

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss']
})
export class CalendarComponent implements OnInit {
  user: User | null = null;
  habits: Habit[] = [];
  logs: HabitLog[] = [];
  isLoading = false;

  view: CalendarView = 'month';
  selectedHabitId: number | 'all' = 'all';
  currentTheme: 'dark' | 'light' = 'dark';

  // Month/Week navigation
  currentDate = new Date();

  // Custom range
  customFrom = '';
  customTo = '';

  // Computed data
  completedLogsSet: Set<string> = new Set();
  monthDays: CalendarDay[] = [];
  weekDays: CalendarDay[] = [];
  yearData: CalendarDay[][] = []; // 7 rows × 52+ cols
  yearMonthLabels: { label: string; col: number }[] = [];

  readonly dayLabels = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
  readonly monthNames = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
                         'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];

  constructor(
    private authService: AuthService,
    private habitService: HabitService,
    private habitLogService: HabitLogService
  ) {}

  ngOnInit(): void {
    const saved = localStorage.getItem('habittracker_theme') as 'dark' | 'light';
    this.currentTheme = saved || 'dark';
    document.documentElement.setAttribute('data-theme', this.currentTheme);

    this.user = this.authService.getCurrentUser();
    if (this.user) {
      this.loadHabits();
    }

    // set default custom range to current month
    const now = new Date();
    this.customFrom = this.toISO(new Date(now.getFullYear(), now.getMonth(), 1));
    this.customTo   = this.toISO(new Date(now.getFullYear(), now.getMonth() + 1, 0));
  }

  logout(): void {
    this.authService.logout();
    this.user = null;
    this.habits = [];
    this.logs = [];
  }

  toggleTheme(): void {
    this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', this.currentTheme);
    localStorage.setItem('habittracker_theme', this.currentTheme);
  }

  loadHabits(): void {
    if (!this.user) return;
    this.habitService.getHabitsByUser(this.user.id).subscribe({
      next: (h) => {
        this.habits = h.filter(x => x.status === 'active');
        this.loadLogs();
      }
    });
  }

  loadLogs(): void {
    if (!this.user) return;
    this.isLoading = true;
    const { from, to } = this.getDateRange();
    this.habitLogService.getLogsByUser(this.user.id, from, to).subscribe({
      next: (logs) => {
        this.logs = logs;
        this.buildDayMap();
        this.buildView();
        this.isLoading = false;
      },
      error: () => { this.isLoading = false; }
    });
  }

  getDateRange(): { from: string; to: string } {
    const d = new Date(this.currentDate);
    if (this.view === 'week') {
      const mon = this.getMonday(d);
      const sun = new Date(mon); sun.setDate(mon.getDate() + 6);
      return { from: this.toISO(mon), to: this.toISO(sun) };
    } else if (this.view === 'month') {
      const from = new Date(d.getFullYear(), d.getMonth(), 1);
      const to   = new Date(d.getFullYear(), d.getMonth() + 1, 0);
      return { from: this.toISO(from), to: this.toISO(to) };
    } else if (this.view === 'year') {
      return {
        from: `${d.getFullYear()}-01-01`,
        to:   `${d.getFullYear()}-12-31`
      };
    } else {
      return { from: this.customFrom, to: this.customTo };
    }
  }

  buildDayMap(): void {
    this.completedLogsSet = new Set();
    const filtered = this.selectedHabitId === 'all'
      ? this.logs
      : this.logs.filter(l => l.habit_id === this.selectedHabitId);
    for (const log of filtered) {
      // Key format: "habitId_YYYY-MM-DD"
      this.completedLogsSet.add(`${log.habit_id}_${log.completed_date}`);
    }
  }

  isHabitScheduledForDate(habit: Habit, date: Date): boolean {
    const dayOfWeek = (date.getDay() + 6) % 7; // 0 = Mon, 6 = Sun
    const dayOfMonth = date.getDate();

    switch (habit.frequency_type) {
      case 'daily':
        return true;
      case 'weekly':
        // Scheduled on Monday by default unless target_days specifies
        if (habit.target_days && habit.target_days.length > 0) {
          return habit.target_days.includes(dayOfWeek);
        }
        return dayOfWeek === 0;
      case 'monthly':
        // Scheduled on the 1st of the month unless target_days specifies
        if (habit.target_days && habit.target_days.length > 0) {
          return habit.target_days.includes(dayOfMonth);
        }
        return dayOfMonth === 1;
      case 'custom':
        if (habit.target_days && habit.target_days.length > 0) {
          return habit.target_days.includes(dayOfWeek);
        }
        return true;
      default:
        return true;
    }
  }

  makeDay(d: Date, inRange: boolean): CalendarDay {
    const key = this.toISO(d);
    const today = this.toISO(new Date());

    const activeHabitsToConsider = this.selectedHabitId === 'all'
      ? this.habits
      : this.habits.filter(h => h.id === this.selectedHabitId);

    const scheduledHabits: DayHabitStatus[] = [];
    let completedCount = 0;

    for (const habit of activeHabitsToConsider) {
      if (this.isHabitScheduledForDate(habit, d)) {
        const isCompleted = this.completedLogsSet.has(`${habit.id}_${key}`);
        if (isCompleted) completedCount++;
        scheduledHabits.push({
          habit,
          completed: isCompleted
        });
      }
    }

    return {
      date: key,
      dateObj: d,
      scheduledHabits,
      completedCount,
      totalScheduled: scheduledHabits.length,
      isToday: key === today,
      isCurrentMonth: d.getMonth() === this.currentDate.getMonth(),
      isInRange: inRange
    };
  }

  intensity(day: CalendarDay): number {
    if (day.totalScheduled === 0) return 0;
    const ratio = day.completedCount / day.totalScheduled;
    if (day.completedCount === 0) return 0;
    if (ratio < 0.35) return 1;
    if (ratio < 0.70) return 2;
    if (ratio < 1)    return 3;
    return 4;
  }

  // ─── Navigation ───────────────────────────────────────────────────────────
  prev(): void {
    const d = new Date(this.currentDate);
    if (this.view === 'week')  d.setDate(d.getDate() - 7);
    if (this.view === 'month') d.setMonth(d.getMonth() - 1);
    if (this.view === 'year')  d.setFullYear(d.getFullYear() - 1);
    this.currentDate = d;
    this.loadLogs();
  }

  next(): void {
    const d = new Date(this.currentDate);
    if (this.view === 'week')  d.setDate(d.getDate() + 7);
    if (this.view === 'month') d.setMonth(d.getMonth() + 1);
    if (this.view === 'year')  d.setFullYear(d.getFullYear() + 1);
    this.currentDate = d;
    this.loadLogs();
  }

  goToday(): void {
    this.currentDate = new Date();
    this.loadLogs();
  }

  onViewChange(): void {
    this.currentDate = new Date();
    this.loadLogs();
  }

  onHabitSelect(val: any): void {
    this.selectedHabitId = val === 'all' ? 'all' : Number(val);
    this.buildDayMap();
    this.buildView();
  }

  onCustomRangeApply(): void {
    if (this.customFrom && this.customTo) this.loadLogs();
  }

  // ─── Helpers ──────────────────────────────────────────────────────────────
  getMonday(d: Date): Date {
    const day = d.getDay();
    const diff = (day === 0 ? -6 : 1 - day);
    const mon = new Date(d);
    mon.setDate(d.getDate() + diff);
    return mon;
  }

  toISO(d: Date): string {
    return d.toISOString().split('T')[0];
  }

  get periodLabel(): string {
    const d = this.currentDate;
    if (this.view === 'week') {
      const mon = this.getMonday(d);
      const sun = new Date(mon); sun.setDate(mon.getDate() + 6);
      return `${mon.getDate()} ${this.monthNames[mon.getMonth()].slice(0,3)} – ${sun.getDate()} ${this.monthNames[sun.getMonth()].slice(0,3)} ${sun.getFullYear()}`;
    }
    if (this.view === 'month') return `${this.monthNames[d.getMonth()]} ${d.getFullYear()}`;
    if (this.view === 'year')  return `${d.getFullYear()}`;
    return `${this.customFrom} → ${this.customTo}`;
  }

  buildView(): void {
    if (this.view === 'week')   this.buildWeek();
    if (this.view === 'month')  this.buildMonth();
    if (this.view === 'year')   this.buildYear();
    if (this.view === 'custom') this.buildMonth();
  }

  buildWeek(): void {
    const mon = this.getMonday(new Date(this.currentDate));
    this.weekDays = [];
    for (let i = 0; i < 7; i++) {
      const d = new Date(mon);
      d.setDate(mon.getDate() + i);
      this.weekDays.push(this.makeDay(d, true));
    }
  }

  buildMonth(): void {
    const d = this.view === 'custom'
      ? new Date(this.customFrom)
      : new Date(this.currentDate);
    const year = d.getFullYear();
    const month = d.getMonth();

    const firstDay = new Date(year, month, 1);
    const lastDay  = new Date(year, month + 1, 0);

    let startPad = firstDay.getDay() - 1;
    if (startPad < 0) startPad = 6;

    this.monthDays = [];
    for (let i = startPad; i > 0; i--) {
      const pd = new Date(firstDay); pd.setDate(pd.getDate() - i);
      this.monthDays.push(this.makeDay(pd, false));
    }
    for (let i = 1; i <= lastDay.getDate(); i++) {
      this.monthDays.push(this.makeDay(new Date(year, month, i), true));
    }
    const endPad = 7 - (this.monthDays.length % 7);
    if (endPad < 7) {
      for (let i = 1; i <= endPad; i++) {
        const nd = new Date(lastDay); nd.setDate(nd.getDate() + i);
        this.monthDays.push(this.makeDay(nd, false));
      }
    }
  }

  buildYear(): void {
    const year = this.currentDate.getFullYear();
    const jan1 = new Date(year, 0, 1);
    let startMon = this.getMonday(jan1);

    const dec31 = new Date(year, 11, 31);
    const allDays: CalendarDay[] = [];
    const cursor = new Date(startMon);
    while (cursor <= dec31 || allDays.length % 7 !== 0) {
      allDays.push(this.makeDay(new Date(cursor), cursor.getFullYear() === year));
      cursor.setDate(cursor.getDate() + 1);
      if (allDays.length > 400) break;
    }

    this.yearData = Array.from({ length: 7 }, () => [] as CalendarDay[]);
    for (let i = 0; i < allDays.length; i++) {
      this.yearData[i % 7].push(allDays[i]);
    }

    this.yearMonthLabels = [];
    let lastMonth = -1;
    for (let col = 0; col < this.yearData[0].length; col++) {
      const day = this.yearData[0][col];
      if (day && day.dateObj.getMonth() !== lastMonth && day.dateObj.getFullYear() === year) {
        this.yearMonthLabels.push({ label: this.monthNames[day.dateObj.getMonth()].slice(0, 3), col });
        lastMonth = day.dateObj.getMonth();
      }
    }
  }

  get totalScheduledInView(): number {
    const days = this.view === 'week' ? this.weekDays : (this.view === 'year' ? this.yearData.flat() : this.monthDays);
    return days.filter(d => d.isInRange).reduce((sum, d) => sum + d.totalScheduled, 0);
  }

  get totalCompletions(): number {
    const days = this.view === 'week' ? this.weekDays : (this.view === 'year' ? this.yearData.flat() : this.monthDays);
    return days.filter(d => d.isInRange).reduce((sum, d) => sum + d.completedCount, 0);
  }

  get activeDays(): number {
    const days = this.view === 'week' ? this.weekDays : (this.view === 'year' ? this.yearData.flat() : this.monthDays);
    return days.filter(d => d.isInRange && d.completedCount > 0).length;
  }

  get weekRows(): CalendarDay[][] {
    const rows: CalendarDay[][] = [];
    for (let i = 0; i < this.monthDays.length; i += 7) {
      rows.push(this.monthDays.slice(i, i + 7));
    }
    return rows;
  }

  get habitName(): string {
    if (this.selectedHabitId === 'all') return 'Todos los hábitos';
    const h = this.habits.find(x => x.id === this.selectedHabitId);
    return h?.title ?? '';
  }

  trackByDate(_: number, d: CalendarDay) { return d.date; }
  trackByIndex(i: number) { return i; }
}
