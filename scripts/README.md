# Wardrobe Assistant Scripts

Helper scripts for efficiently managing and querying your wardrobe data.

## Overview

These Python scripts provide command-line tools for working with your wardrobe data. They're designed to be used by both humans (via terminal) and the StyleBot agent (via automated workflows).

## Scripts

### 1. `wardrobe_query.py`
**Query and filter wardrobe items efficiently**

Instead of loading the entire 40K+ token wardrobe file, this script uses the lightweight index for fast filtering.

```bash
# Find all summer tops with formality 5-7
python scripts/wardrobe_query.py --type tops --formality 5-7 --season summer

# Find navy button-up shirts
python scripts/wardrobe_query.py --category "button-up shirt" --color navy

# Get specific items with full details
python scripts/wardrobe_query.py --ids item_20251004_001 item_20251004_002 --detailed

# List all sneakers in summary format
python scripts/wardrobe_query.py --category sneakers --format summary

# Get just IDs (useful for piping to other commands)
python scripts/wardrobe_query.py --category jeans --format ids
```

**Options:**
- `--type` - Filter by type (tops, bottoms, shoes, outerwear, accessories)
- `--category` - Filter by category (e.g., "button-up shirt", "jeans", "sneakers")
- `--color` - Filter by primary color
- `--formality` - Filter by formality range (e.g., "5-7" or "6")
- `--season` - Filter by season (spring, summer, fall, winter)
- `--tag` - Filter by tag
- `--ids` - Get specific items by ID(s)
- `--all` - Return all items
- `--detailed` - Include full item details (loads from wardrobe_items.json)
- `--format` - Output format: `json` (default), `summary`, or `ids`

---

### 2. `generate_recommendation_html.py`
**Convert recommendation JSON to beautiful HTML visualization**

Takes a recommendation JSON file and generates a styled HTML page with outfit images, color palettes, and reasoning.

```bash
# Generate HTML for a recommendation
python scripts/generate_recommendation_html.py rec_20251005_001

# Generate with custom output path
python scripts/generate_recommendation_html.py rec_20251005_001 --output my_outfit.html
```

**Features:**
- Displays all outfit options with images
- Shows color palettes with visual swatches
- Includes reasoning and styling notes
- Alternative suggestions
- Responsive design for mobile/desktop

**Output:** Saves to `data/recommendations/{id}.html` (or custom path)

---

### 3. `get_item_details.py`
**Retrieve full details for specific items by ID**

Fetch complete information about wardrobe items without loading the entire wardrobe.

```bash
# Get details for one item
python scripts/get_item_details.py item_20251004_001

# Get details for multiple items
python scripts/get_item_details.py item_20251004_001 item_20251004_002

# Get human-readable summary
python scripts/get_item_details.py item_20251004_001 --format summary

# Get compact one-line format
python scripts/get_item_details.py item_20251004_001 item_20251004_002 --format compact
```

**Output formats:**
- `json` - Full JSON details (default)
- `summary` - Human-readable formatted output
- `compact` - One-line summaries for quick scanning

---

### 4. `update_wardrobe.py`
**Update, remove, or modify wardrobe items**

Make programmatic changes to your wardrobe while keeping both `wardrobe_items.json` and `wardrobe_index.json` in sync.

```bash
# Update formality level
python scripts/update_wardrobe.py --update item_20251004_001 --field metadata.formality --value 7

# Update wear count
python scripts/update_wardrobe.py --update item_20251004_001 --field tracking.wearCount --value 5

# Mark items as worn (increments wearCount, sets lastWorn)
python scripts/update_wardrobe.py --mark-worn item_20251004_001 item_20251004_002

# Remove an item
python scripts/update_wardrobe.py --remove item_20251004_001

# Update item name
python scripts/update_wardrobe.py --update item_20251004_001 --field name --value "New Item Name"
```

**Safety features:**
- Automatically keeps index in sync with full wardrobe
- Updates `lastUpdated` timestamp
- Validates items exist before modifying
- Supports nested field updates using dot notation

**Note:** For adding new items, use the StyleBot agent's `*add-item` command which includes AI vision analysis.

---

## Usage in StyleBot Agent

The StyleBot agent uses these scripts internally to:

1. **Filter wardrobe efficiently** - Instead of loading 40K+ tokens, query the index
2. **Generate HTML visualizations** - Create beautiful outfit pages automatically
3. **Update tracking data** - Mark items as worn after feedback
4. **Retrieve specific items** - Get details only for relevant items

This keeps context usage low and responses fast!

---

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

---

## File Paths

Scripts expect the following project structure:

```
my-wardrobe-assistant/
├── scripts/
│   ├── wardrobe_query.py
│   ├── get_item_details.py
│   ├── generate_recommendation_html.py
│   └── update_wardrobe.py
├── data/
│   ├── wardrobe/
│   │   ├── wardrobe_index.json
│   │   └── wardrobe_items.json
│   ├── recommendations/
│   │   └── *.json, *.html
│   └── feedback/
│       └── *.json
└── templates/
    └── recommendations/
        └── recommendation.html
```

All scripts automatically resolve paths relative to the project root, so you can run them from anywhere.

---

## Examples

### Common Workflows

**Find outfit pieces for a casual dinner:**
```bash
# Find smart-casual tops
python scripts/wardrobe_query.py --type tops --formality 5-7 --season summer --format summary

# Find matching bottoms
python scripts/wardrobe_query.py --type bottoms --formality 5-6 --season summer --format summary

# Get full details of chosen items
python scripts/get_item_details.py item_20251004_059 item_20251004_027 --format summary
```

**After wearing an outfit:**
```bash
# Mark items as worn
python scripts/update_wardrobe.py --mark-worn item_20251004_059 item_20251004_027 item_20251004_037
```

**Generate a shareable outfit page:**
```bash
# Create HTML visualization
python scripts/generate_recommendation_html.py rec_20251005_001

# Open in browser (Windows)
start data/recommendations/rec_20251005_001.html

# Open in browser (Mac)
open data/recommendations/rec_20251005_001.html
```

---

## Troubleshooting

**"File not found" errors:**
- Make sure you're running from the project root, or scripts will auto-detect path
- Check that `data/wardrobe/` directory exists

**"Item not found" warnings:**
- Verify item IDs are correct using `--format ids` to list all IDs
- Check that wardrobe_items.json and wardrobe_index.json are in sync

**JSON parsing errors:**
- Validate your JSON files at [jsonlint.com](https://jsonlint.com)
- Common issue: trailing commas in JSON (not allowed)

---

## Contributing

These scripts are designed to be simple, standalone, and require no dependencies. When modifying:

1. Keep standard library only (no external packages)
2. Maintain backward compatibility with existing data formats
3. Update this README with new examples
4. Test with actual wardrobe data

---

## License

Part of the My Wardrobe Assistant project. See main README for license information.
