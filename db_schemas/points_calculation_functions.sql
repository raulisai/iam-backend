-- =====================================================
-- POINTS CALCULATION FUNCTIONS
-- =====================================================
-- Functions to calculate points from pending tasks
-- =====================================================

-- Function to calculate total reward_xp from pending tasks in a specific table
CREATE OR REPLACE FUNCTION public.calculate_pending_points(
  p_user_id UUID,
  p_table_name TEXT
)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
DECLARE
  v_total_points NUMERIC := 0;
  v_query TEXT;
BEGIN
  -- Validate table name to prevent SQL injection
  IF p_table_name NOT IN ('tasks_mind', 'tasks_body') THEN
    RAISE EXCEPTION 'Invalid table name: %', p_table_name;
  END IF;

  -- Build dynamic query to sum reward_xp from pending tasks
  v_query := format('
    SELECT COALESCE(SUM(tt.reward_xp), 0)
    FROM public.%I t
    JOIN public.task_templates tt ON tt.id = t.template_id
    WHERE t.user_id = $1
      AND t.status = ''pending''
  ', p_table_name);

  -- Execute the query
  EXECUTE v_query INTO v_total_points USING p_user_id;

  RETURN v_total_points;
END;
$$;

-- Comment
COMMENT ON FUNCTION public.calculate_pending_points(UUID, TEXT) IS 
'Calculates total reward_xp from pending tasks in tasks_mind or tasks_body tables';


-- =====================================================
-- AUTOMATIC POINTS UPDATE TRIGGERS
-- =====================================================
-- Triggers to automatically update goal_points_target when tasks change
-- =====================================================

-- Function to recalculate goal_points_target when mind or body tasks change
CREATE OR REPLACE FUNCTION public.trg_update_goal_points_target()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
  v_user_id UUID;
  v_mind_points NUMERIC;
  v_body_points NUMERIC;
  v_goal_points NUMERIC;
  v_total_points NUMERIC;
BEGIN
  -- Determine the user_id (works for INSERT, UPDATE, DELETE)
  IF TG_OP = 'DELETE' THEN
    v_user_id := OLD.user_id;
  ELSE
    v_user_id := NEW.user_id;
  END IF;

  -- Calculate points from mind tasks
  SELECT public.calculate_pending_points(v_user_id, 'tasks_mind') INTO v_mind_points;
  
  -- Calculate points from body tasks
  SELECT public.calculate_pending_points(v_user_id, 'tasks_body') INTO v_body_points;
  
  -- Calculate points from goal tasks (simplified - count all active goal_tasks weights)
  SELECT COALESCE(SUM(gt.weight), 0) INTO v_goal_points
  FROM public.goal_tasks gt
  JOIN public.goals g ON g.id = gt.goal_id
  WHERE gt.user_id = v_user_id AND g.is_active = TRUE;
  
  -- Total points
  v_total_points := v_mind_points + v_body_points + v_goal_points;
  
  -- Update profile
  UPDATE public.profiles
  SET goal_points_target = v_total_points,
      updated_at = NOW()
  WHERE user_id = v_user_id;
  
  RETURN NEW;
END;
$$;

-- Create triggers for tasks_mind
DROP TRIGGER IF EXISTS tasks_mind_points_update_trg ON public.tasks_mind;
CREATE TRIGGER tasks_mind_points_update_trg
AFTER INSERT OR UPDATE OR DELETE ON public.tasks_mind
FOR EACH ROW
EXECUTE FUNCTION public.trg_update_goal_points_target();

-- Create triggers for tasks_body
DROP TRIGGER IF EXISTS tasks_body_points_update_trg ON public.tasks_body;
CREATE TRIGGER tasks_body_points_update_trg
AFTER INSERT OR UPDATE OR DELETE ON public.tasks_body
FOR EACH ROW
EXECUTE FUNCTION public.trg_update_goal_points_target();

-- Create triggers for goal_tasks
DROP TRIGGER IF EXISTS goal_tasks_points_update_trg ON public.goal_tasks;
CREATE TRIGGER goal_tasks_points_update_trg
AFTER INSERT OR UPDATE OR DELETE ON public.goal_tasks
FOR EACH ROW
EXECUTE FUNCTION public.trg_update_goal_points_target();

-- Comment
COMMENT ON FUNCTION public.trg_update_goal_points_target() IS 
'Automatically recalculates and updates goal_points_target in profiles when tasks change';
