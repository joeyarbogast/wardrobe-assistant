#!/usr/bin/env python3
"""
Get Item Details
Retrieve full details for specific wardrobe items by ID.

Usage:
    python scripts/get_item_details.py item_20251004_001
    python scripts/get_item_details.py item_20251004_001 item_20251004_002 item_20251004_003
    python scripts/get_item_details.py item_20251004_001 --format summary
"""

import json
import argparse
import sys
from pathlib import Path

# Set base path to project root
BASE_PATH = Path(__file__).parent.parent
WARDROBE_ITEMS = BASE_PATH / "data" / "wardrobe" / "wardrobe_items.json"


def load_wardrobe():
    """Load full wardrobe items."""
    with open(WARDROBE_ITEMS, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_items_by_ids(item_ids):
    """Retrieve items by their IDs."""
    data = load_wardrobe()
    items = data['items']

    # Create lookup for fast access
    item_map = {item['id']: item for item in items}

    # Get requested items
    found_items = []
    not_found = []

    for item_id in item_ids:
        if item_id in item_map:
            found_items.append(item_map[item_id])
        else:
            not_found.append(item_id)

    return found_items, not_found


def format_json(items):
    """Format as JSON."""
    print(json.dumps(items, indent=2))


def format_summary(items):
    """Format as human-readable summary."""
    for item in items:
        print(f"\n{'='*80}")
        print(f"ID: {item.get('id', 'N/A')}")
        print(f"Name: {item.get('name', 'N/A')}")
        print(f"Brand: {item.get('brand', 'N/A')}")
        print(f"Type: {item.get('type', 'N/A')} / {item.get('category', 'N/A')}")
        print(f"{'='*80}")

        # Metadata
        metadata = item.get('metadata', {})
        colors = metadata.get('colors', {})
        print(f"\nColors:")
        print(f"  Primary: {colors.get('primary', 'N/A')}")
        if colors.get('secondary'):
            print(f"  Secondary: {', '.join(colors.get('secondary', []))}")
        if colors.get('accent'):
            print(f"  Accent: {', '.join(colors.get('accent', []))}")

        print(f"\nMaterial: {metadata.get('material', 'N/A')}")
        print(f"Fit: {metadata.get('fit', 'N/A')}")
        print(f"Formality: {metadata.get('formality', 'N/A')}/10")

        patterns = metadata.get('patterns', [])
        if patterns:
            print(f"Patterns: {', '.join(patterns)}")

        style = metadata.get('style', [])
        if style:
            print(f"Style: {', '.join(style)}")

        # Context
        context = item.get('context', {})
        seasons = context.get('seasons', [])
        if seasons:
            print(f"\nSeasons: {', '.join(seasons)}")

        occasions = context.get('occasions', [])
        if occasions:
            print(f"Occasions: {', '.join(occasions)}")

        # Tracking
        tracking = item.get('tracking', {})
        print(f"\nWear Count: {tracking.get('wearCount', 0)}")
        last_worn = tracking.get('lastWorn')
        if last_worn:
            print(f"Last Worn: {last_worn}")

        # Image
        img_path = item.get('imagePath')
        if img_path:
            print(f"\nImage: {img_path}")

        # Notes
        notes = item.get('notes')
        if notes:
            print(f"\nNotes: {notes}")

        # Tags
        tags = item.get('tags', [])
        if tags:
            print(f"Tags: {', '.join(tags)}")

        print()


def format_compact(items):
    """Format as compact one-line summaries."""
    for item in items:
        metadata = item.get('metadata', {})
        colors = metadata.get('colors', {})
        formality = metadata.get('formality', 'N/A')

        print(f"{item.get('id', 'N/A'):25} | "
              f"{item.get('name', 'N/A'):50} | "
              f"{item.get('category', 'N/A'):20} | "
              f"{colors.get('primary', 'N/A'):15} | "
              f"F:{formality}")


def main():
    parser = argparse.ArgumentParser(
        description='Get full details for specific wardrobe items',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get details for one item
  python scripts/get_item_details.py item_20251004_001

  # Get details for multiple items
  python scripts/get_item_details.py item_20251004_001 item_20251004_002

  # Get summary format
  python scripts/get_item_details.py item_20251004_001 --format summary

  # Get compact format
  python scripts/get_item_details.py item_20251004_001 item_20251004_002 --format compact
        """
    )

    parser.add_argument('item_ids', nargs='+', help='Item ID(s) to retrieve')
    parser.add_argument('--format', choices=['json', 'summary', 'compact'], default='json',
                       help='Output format (default: json)')

    args = parser.parse_args()

    # Get items
    found_items, not_found = get_items_by_ids(args.item_ids)

    # Warn about not found items
    if not_found:
        print(f"Warning: {len(not_found)} item(s) not found:", file=sys.stderr)
        for item_id in not_found:
            print(f"  - {item_id}", file=sys.stderr)
        print(file=sys.stderr)

    # Format output
    if not found_items:
        print("No items found.", file=sys.stderr)
        sys.exit(1)

    if args.format == 'json':
        format_json(found_items)
    elif args.format == 'summary':
        format_summary(found_items)
    elif args.format == 'compact':
        format_compact(found_items)


if __name__ == '__main__':
    main()
