export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
}

export interface LoginRequest {
  username_or_email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export type FrequencyType = 'daily' | 'weekly' | 'monthly' | 'custom';
export type HabitStatus = 'active' | 'archived' | 'deleted';

export interface Habit {
  id: number;
  user_id: number;
  title: string;
  description?: string;
  frequency_type: FrequencyType;
  target_days?: number[];
  status: HabitStatus;
}

export interface HabitCreate {
  user_id: number;
  title: string;
  description?: string;
  frequency_type: FrequencyType;
  target_days?: number[];
}

export interface HabitUpdate {
  title?: string;
  description?: string;
  frequency_type?: FrequencyType;
  target_days?: number[];
  status?: HabitStatus;
}

export interface HabitLog {
  id: number;
  habit_id: number;
  completed_date: string;
  notes?: string;
}

export interface HabitLogCreate {
  habit_id: number;
  notes?: string;
}

export interface Streak {
  id: number;
  habit_id: number;
  current_streak: number;
  longest_streak: number;
  last_completed_date?: string;
}
