-- Profile schema migration
-- Add time_dead and day_work columns to profiles table

-- Add the time_dead column if it doesn't exist
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS time_dead NUMERIC DEFAULT 0;

COMMENT ON COLUMN public.profiles.time_dead IS 'Time dead or unproductive time tracked for the user';

-- Add the day_work column if it doesn't exist
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS day_work TEXT DEFAULT NULL;

COMMENT ON COLUMN public.profiles.day_work IS 'Work days in the week (D,L,M,M,J,V,S format)';
