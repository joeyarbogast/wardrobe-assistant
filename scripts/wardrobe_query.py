#!/usr/bin/env python3
"""
Wardrobe Query Tool
Efficiently filter and search wardrobe items without loading the full wardrobe file.

Usage:
    python scripts/wardrobe_query.py --type tops --formality 5-7 --season summer
    python scripts/wardrobe_query.py --category "button-up shirt" --color navy
    python scripts/wardrobe_query.py --ids item_20251004_001 item_20251004_002
    python scripts/wardrobe_query.py --all --detailed
"""

import json
import argparse
import sys
from pathlib import Path

# Set base path to project root
BASE_PATH = Path(__file__).parent.parent
WARDROBE_INDEX = BASE_PATH / "data" / "wardrobe" / "wardrobe_index.json"
WARDROBE_ITEMS = BASE_PATH / "data" / "wardrobe" / "wardrobe_items.json"


def load_index():
    """Load the lightweight wardrobe index."""
    with open(WARDROBE_INDEX, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_full_items(item_ids=None):
    """Load full item details from wardrobe_items.json.

    Args:
        item_ids: Optional list of item IDs to filter by. If None, loads all items.
    """
    with open(WARDROBE_ITEMS, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if item_ids:
        # Filter to only requested IDs
        filtered = [item for item in data['items'] if item['id'] in item_ids]
        return filtered

    return data['items']


def parse_formality_range(formality_str):
    """Parse formality string like '5-7' or '6' into min/max range."""
    if '-' in formality_str:
        min_f, max_f = formality_str.split('-')
        return int(min_f), int(max_f)
    else:
        f = int(formality_str)
        return f, f


def filter_index(index_data, args):
    """Filter index based on provided arguments."""
    items = index_data['items']
    filtered = items

    # Filter by type
    if args.type:
        filtered = [item for item in filtered if item.get('type', '').lower() == args.type.lower()]

    # Filter by category
    if args.category:
        filtered = [item for item in filtered if item.get('category', '').lower() == args.category.lower()]

    # Filter by primary color
    if args.color:
        filtered = [item for item in filtered
                   if args.color.lower() in item.get('primaryColor', '').lower()]

    # Filter by formality range
    if args.formality:
        min_f, max_f = parse_formality_range(args.formality)
        filtered = [item for item in filtered
                   if min_f <= item.get('formality', 0) <= max_f]

    # Filter by season
    if args.season:
        filtered = [item for item in filtered
                   if args.season.lower() in [s.lower() for s in item.get('seasons', [])]]

    # Filter by tags
    if args.tag:
        filtered = [item for item in filtered
                   if args.tag.lower() in [t.lower() for t in item.get('tags', [])]]

    # Filter by IDs
    if args.ids:
        id_set = set(args.ids)
        filtered = [item for item in filtered if item['id'] in id_set]

    return filtered


def format_output(items, detailed=False, output_format='json'):
    """Format output based on requested format."""
    if output_format == 'json':
        print(json.dumps(items, indent=2))

    elif output_format == 'summary':
        print(f"\n{'='*80}")
        print(f"Found {len(items)} items")
        print(f"{'='*80}\n")

        for item in items:
            print(f"ID: {item.get('id', 'N/A')}")
            print(f"Name: {item.get('name', 'N/A')}")
            print(f"Type: {item.get('type', 'N/A')} / {item.get('category', 'N/A')}")
            print(f"Color: {item.get('primaryColor', item.get('metadata', {}).get('colors', {}).get('primary', 'N/A'))}")
            print(f"Formality: {item.get('formality', item.get('metadata', {}).get('formality', 'N/A'))}")

            if detailed:
                seasons = item.get('seasons', item.get('context', {}).get('seasons', []))
                print(f"Seasons: {', '.join(seasons) if seasons else 'N/A'}")
                tags = item.get('tags', [])
                if tags:
                    print(f"Tags: {', '.join(tags)}")

            print(f"{'-'*80}\n")

    elif output_format == 'ids':
        # Just print IDs, one per line (useful for piping)
        for item in items:
            print(item.get('id', ''))


def main():
    parser = argparse.ArgumentParser(
        description='Query wardrobe items efficiently',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find all summer tops with formality 5-7
  python scripts/wardrobe_query.py --type tops --formality 5-7 --season summer

  # Find navy button-up shirts
  python scripts/wardrobe_query.py --category "button-up shirt" --color navy

  # Get specific items by ID with full details
  python scripts/wardrobe_query.py --ids item_20251004_001 item_20251004_002 --detailed

  # List all sneakers
  python scripts/wardrobe_query.py --category sneakers --format summary

  # Get just IDs of all jeans (for piping)
  python scripts/wardrobe_query.py --category jeans --format ids
        """
    )

    # Filter arguments
    parser.add_argument('--type', help='Filter by type (tops, bottoms, shoes, outerwear, accessories)')
    parser.add_argument('--category', help='Filter by category (e.g., "button-up shirt", "jeans", "sneakers")')
    parser.add_argument('--color', help='Filter by primary color')
    parser.add_argument('--formality', help='Filter by formality range (e.g., "5-7" or "6")')
    parser.add_argument('--season', help='Filter by season (spring, summer, fall, winter)')
    parser.add_argument('--tag', help='Filter by tag')
    parser.add_argument('--ids', nargs='+', help='Get specific items by ID(s)')
    parser.add_argument('--all', action='store_true', help='Return all items (no filtering)')

    # Output options
    parser.add_argument('--detailed', action='store_true', help='Include full item details (requires loading wardrobe_items.json)')
    parser.add_argument('--format', choices=['json', 'summary', 'ids'], default='json',
                       help='Output format (default: json)')

    args = parser.parse_args()

    # If --all and not --detailed, just return index
    if args.all and not args.detailed:
        index_data = load_index()
        items = index_data['items']
        format_output(items, detailed=False, output_format=args.format)
        return

    # Load and filter index
    index_data = load_index()
    filtered_items = filter_index(index_data, args)

    # If detailed output requested, load full items
    if args.detailed:
        item_ids = [item['id'] for item in filtered_items]
        full_items = load_full_items(item_ids)
        format_output(full_items, detailed=True, output_format=args.format)
    else:
        format_output(filtered_items, detailed=False, output_format=args.format)


if __name__ == '__main__':
    main()
