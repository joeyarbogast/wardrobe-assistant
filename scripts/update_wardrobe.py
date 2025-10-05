#!/usr/bin/env python3
"""
Wardrobe Update Tool
Add, update, or remove items from the wardrobe while keeping index in sync.

Usage:
    # Update an existing item
    python scripts/update_wardrobe.py --update item_20251004_001 --field wearCount --value 5

    # Remove an item
    python scripts/update_wardrobe.py --remove item_20251004_001

    # Update last worn date
    python scripts/update_wardrobe.py --mark-worn item_20251004_001 item_20251004_002

Note: Adding items is better done through the StyleBot agent's *add-item command
      which includes AI vision analysis. This script is for programmatic updates.
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime

# Set base path to project root
BASE_PATH = Path(__file__).parent.parent
WARDROBE_INDEX = BASE_PATH / "data" / "wardrobe" / "wardrobe_index.json"
WARDROBE_ITEMS = BASE_PATH / "data" / "wardrobe" / "wardrobe_items.json"


def load_json(filepath):
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath, data):
    """Save JSON file with proper formatting."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def find_item_by_id(items, item_id):
    """Find item in list by ID."""
    for idx, item in enumerate(items):
        if item.get('id') == item_id:
            return idx, item
    return None, None


def update_item_field(item_id, field_path, value):
    """Update a specific field in an item.

    Args:
        item_id: Item ID to update
        field_path: Dot-notation path to field (e.g., 'metadata.formality' or 'tracking.wearCount')
        value: New value
    """
    # Load data
    items_data = load_json(WARDROBE_ITEMS)
    index_data = load_json(WARDROBE_INDEX)

    # Find item in full wardrobe
    idx, item = find_item_by_id(items_data['items'], item_id)
    if idx is None:
        print(f"Error: Item {item_id} not found in wardrobe_items.json", file=sys.stderr)
        return False

    # Update field using dot notation
    field_parts = field_path.split('.')
    current = item

    # Navigate to parent of field
    for part in field_parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]

    # Set the value
    final_field = field_parts[-1]
    old_value = current.get(final_field)
    current[final_field] = value

    # Update lastUpdated timestamp
    if 'tracking' not in item:
        item['tracking'] = {}
    item['tracking']['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'

    # Save full wardrobe
    save_json(WARDROBE_ITEMS, items_data)

    # Update index if necessary (only certain fields are in index)
    index_fields = ['name', 'type', 'category', 'formality', 'seasons', 'tags']

    # Check if updated field affects index
    update_index = False
    if field_parts[0] in index_fields:
        update_index = True
    elif field_parts[0] == 'metadata' and len(field_parts) > 1:
        if field_parts[1] in ['formality']:
            update_index = True
        elif field_parts[1] == 'colors' and len(field_parts) > 2 and field_parts[2] == 'primary':
            update_index = True

    if update_index:
        # Find and update in index
        idx_idx, idx_item = find_item_by_id(index_data['items'], item_id)
        if idx_idx is not None:
            # Rebuild index entry from full item
            metadata = item.get('metadata', {})
            colors = metadata.get('colors', {})
            context = item.get('context', {})

            index_data['items'][idx_idx] = {
                'id': item['id'],
                'name': item['name'],
                'type': item['type'],
                'category': item['category'],
                'primaryColor': colors.get('primary', ''),
                'formality': metadata.get('formality', 0),
                'seasons': context.get('seasons', []),
                'tags': item.get('tags', [])
            }

            save_json(WARDROBE_INDEX, index_data)
            print(f"Updated index for {item_id}")

    print(f"Updated {item_id}: {field_path} = {value} (was: {old_value})")
    return True


def remove_item(item_id):
    """Remove an item from both wardrobe and index."""
    # Load data
    items_data = load_json(WARDROBE_ITEMS)
    index_data = load_json(WARDROBE_INDEX)

    # Find and remove from full wardrobe
    idx, item = find_item_by_id(items_data['items'], item_id)
    if idx is None:
        print(f"Error: Item {item_id} not found in wardrobe_items.json", file=sys.stderr)
        return False

    item_name = item.get('name', item_id)
    items_data['items'].pop(idx)
    save_json(WARDROBE_ITEMS, items_data)

    # Find and remove from index
    idx_idx, idx_item = find_item_by_id(index_data['items'], item_id)
    if idx_idx is not None:
        index_data['items'].pop(idx_idx)
        save_json(WARDROBE_INDEX, index_data)

    print(f"Removed item: {item_name} ({item_id})")
    print(f"  - Removed from wardrobe_items.json")
    print(f"  - Removed from wardrobe_index.json")
    return True


def mark_items_worn(item_ids, wear_date=None):
    """Mark items as worn by updating wearCount and lastWorn.

    Args:
        item_ids: List of item IDs to mark as worn
        wear_date: Date worn (ISO format). Defaults to current UTC time.
    """
    if wear_date is None:
        wear_date = datetime.utcnow().isoformat() + 'Z'

    # Load data
    items_data = load_json(WARDROBE_ITEMS)

    updated_count = 0
    for item_id in item_ids:
        idx, item = find_item_by_id(items_data['items'], item_id)
        if idx is None:
            print(f"Warning: Item {item_id} not found, skipping", file=sys.stderr)
            continue

        # Update tracking
        if 'tracking' not in item:
            item['tracking'] = {}

        tracking = item['tracking']
        tracking['wearCount'] = tracking.get('wearCount', 0) + 1
        tracking['lastWorn'] = wear_date
        tracking['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'

        updated_count += 1
        print(f"Marked {item.get('name', item_id)} as worn (total: {tracking['wearCount']})")

    if updated_count > 0:
        save_json(WARDROBE_ITEMS, items_data)
        print(f"\nUpdated {updated_count} item(s)")

    return updated_count > 0


def main():
    parser = argparse.ArgumentParser(
        description='Update wardrobe items (add, update, remove)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update formality level
  python scripts/update_wardrobe.py --update item_20251004_001 --field metadata.formality --value 7

  # Update wear count
  python scripts/update_wardrobe.py --update item_20251004_001 --field tracking.wearCount --value 5

  # Mark items as worn (increments wearCount, updates lastWorn)
  python scripts/update_wardrobe.py --mark-worn item_20251004_001 item_20251004_002

  # Remove an item
  python scripts/update_wardrobe.py --remove item_20251004_001

  # Update item name
  python scripts/update_wardrobe.py --update item_20251004_001 --field name --value "New Item Name"
        """
    )

    # Action arguments (mutually exclusive)
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--update', metavar='ITEM_ID', help='Update a field in an item')
    action_group.add_argument('--remove', metavar='ITEM_ID', help='Remove an item')
    action_group.add_argument('--mark-worn', nargs='+', metavar='ITEM_ID',
                             help='Mark item(s) as worn (increments wearCount)')

    # Update-specific arguments
    parser.add_argument('--field', help='Field path to update (e.g., metadata.formality)')
    parser.add_argument('--value', help='New value for field')

    # Optional arguments
    parser.add_argument('--date', help='Date for --mark-worn (ISO format, default: now)')

    args = parser.parse_args()

    # Validate arguments
    if args.update and (not args.field or not args.value):
        parser.error('--update requires both --field and --value')

    # Execute action
    if args.update:
        # Try to convert value to appropriate type
        value = args.value
        try:
            # Try int
            value = int(value)
        except ValueError:
            try:
                # Try float
                value = float(value)
            except ValueError:
                # Try boolean
                if value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                # Otherwise keep as string

        success = update_item_field(args.update, args.field, value)
        sys.exit(0 if success else 1)

    elif args.remove:
        success = remove_item(args.remove)
        sys.exit(0 if success else 1)

    elif args.mark_worn:
        success = mark_items_worn(args.mark_worn, args.date)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
