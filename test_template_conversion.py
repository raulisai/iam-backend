"""
Test script to verify template key to UUID conversion
"""
from services.task_template_service import get_task_template_by_key, get_all_task_templates

print("=" * 60)
print("Testing Template Key to UUID Conversion")
print("=" * 60)

# Get all templates
print("\n1. Getting all templates...")
templates = get_all_task_templates()
print(f"   Found {len(templates)} templates")

# Show first 5 templates
print("\n2. Sample templates:")
for i, template in enumerate(templates[:5]):
    print(f"   {i+1}. Key: '{template.get('key')}' -> UUID: {template.get('id')}")
    print(f"      Name: {template.get('name')}")
    print(f"      Category: {template.get('category')}")
    print()

# Test conversion for a specific key
print("\n3. Testing conversion for specific keys:")
test_keys = ['meditation_15', 'daily_reading_01', 'morning_run_01', 'journal_writing_01']

for key in test_keys:
    template = get_task_template_by_key(key)
    if template:
        print(f"   ✅ '{key}' -> UUID: {template.get('id')}")
        print(f"      Name: {template.get('name')}")
    else:
        print(f"   ❌ '{key}' -> NOT FOUND")
    print()

print("=" * 60)
print("Test Complete!")
print("=" * 60)
