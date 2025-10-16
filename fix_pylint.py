"""Fix pylint errors in routine files."""
import os

files_to_fix = [
    'controllers/routine_alarm_controller.py',
    'controllers/routine_reminder_controller.py',
    'services/routine_alarm_service.py',
    'services/routine_reminder_service.py',
    'routes/routine_reminder_routes.py'
]

for file_path in files_to_fix:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remove trailing whitespace from each line
    cleaned_lines = [line.rstrip() + '\n' for line in lines]
    
    # Ensure file ends with newline
    if cleaned_lines and not cleaned_lines[-1].endswith('\n'):
        cleaned_lines[-1] += '\n'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    print(f"Fixed: {file_path}")

print("Done!")
