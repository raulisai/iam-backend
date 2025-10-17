-- =====================================================
-- PROFILES TABLE MIGRATION - Add Goal Points Tracking
-- =====================================================
-- Migration to add goal points tracking to profiles
-- =====================================================

-- Add new columns for goal points tracking
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS goal_points_target NUMERIC NOT NULL DEFAULT 0,
ADD COLUMN IF NOT EXISTS goal_points_earned NUMERIC NOT NULL DEFAULT 0;

-- Add comments
COMMENT ON COLUMN public.profiles.goal_points_target IS 'Total points available from all active goals and tasks';
COMMENT ON COLUMN public.profiles.goal_points_earned IS 'Points earned from completed tasks';

-- Add check constraints to ensure non-negative values
ALTER TABLE public.profiles 
ADD CONSTRAINT check_goal_points_target_non_negative CHECK (goal_points_target >= 0),
ADD CONSTRAINT check_goal_points_earned_non_negative CHECK (goal_points_earned >= 0);
