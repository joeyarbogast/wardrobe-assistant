# Wardrobe Data Structure

This directory uses an **index-based architecture** for efficient wardrobe management that scales to hundreds of items.

## Files

### `wardrobe_index.json` (Required - Your Actual Data)
Lightweight index with minimal metadata per item. **Load this file first** to filter and find items.

**Fields in index:**
- `id` - Unique identifier
- `name` - Display name
- `type` - Category: tops, bottoms, outerwear, shoes, accessories
- `category` - Subcategory: shirt, pants, jacket, etc.
- `primaryColor` - Main color for filtering
- `formality` - 1-10 scale (1=casual, 10=formal)
- `seasons` - Array: spring, summer, fall, winter
- `tags` - Quick reference tags

**Size:** ~100-200 bytes per item (~50KB for 500 items)

### `wardrobe_items.json` (Required - Your Actual Data)
Complete details for all wardrobe items. **Load specific items from this file** after filtering the index.

**Contains full metadata:**
- All fields from index
- Complete color information (primary, secondary, accent)
- Patterns, material, fit, style
- Context (weather ranges, occasions, time of day)
- Tracking (dates added/worn, wear count)
- Image paths
- Notes and tags
- AI analysis

**Size:** ~1.5KB per item (~750KB for 500 items)

### `wardrobe_index.template.json` (Template - For Reference)
Example structure showing what the index should look like. **Copy this to `wardrobe_index.json`** when starting your wardrobe.

### `wardrobe_items.template.json` (Template - For Reference)
Example structure showing complete item details. **Copy this to `wardrobe_items.json`** when starting your wardrobe.

## Why This Architecture?

### The Problem
- Individual files per item: 500 items = 500 file reads = context overflow
- Single monolithic file: Must load ALL items even when you only need "blue summer shirts"

### The Solution: Index + Items Pattern
1. **Filter First**: Load lightweight index (~50KB), filter to relevant items
2. **Fetch Details**: Load only the 5-10 matching items from `wardrobe_items.json`
3. **Stay Efficient**: Claude's context focused on relevant items only

### Scalability

| Wardrobe Size | Index Size | Items File Size | Context Used (typical query) |
|---------------|------------|-----------------|------------------------------|
| 50 items      | ~10KB      | ~75KB          | ~20KB (index + 5 items)      |
| 100 items     | ~20KB      | ~150KB         | ~25KB (index + 5 items)      |
| 200 items     | ~40KB      | ~300KB         | ~30KB (index + 5 items)      |
| 500 items     | ~100KB     | ~750KB         | ~40KB (index + 10 items)     |

**Without index:** Would need to load entire items file every time (75KB-750KB).

## Workflow Examples

### Example 1: Find Blue Shirts for Summer
```javascript
// 1. Load and filter index
const index = loadJSON('wardrobe_index.json')
const matches = index.filter(item =>
  item.type === 'tops' &&
  item.primaryColor.includes('blue') &&
  item.seasons.includes('summer')
)
// Result: [item_001, item_045, item_092]

// 2. Load only those items from wardrobe_items.json
const fullItems = loadJSON('wardrobe_items.json')
const details = fullItems.items.filter(item =>
  matches.includes(item.id)
)
// Now have full details for just 3 items instead of all 500
```

### Example 2: Build Outfit for Business Casual Event
```javascript
// 1. Filter index by formality and season
const index = loadJSON('wardrobe_index.json')
const candidates = index.filter(item =>
  item.formality >= 6 && item.formality <= 8 &&
  item.seasons.includes('fall')
)

// 2. Load full details for candidates
// 3. Apply advanced filtering (color coordination, etc.)
// 4. Build outfit from filtered set
```

## Getting Started

### 1. First Time Setup
```bash
# Copy templates to create your actual data files
cp wardrobe_index.template.json wardrobe_index.json
cp wardrobe_items.template.json wardrobe_items.json
```

### 2. Adding Items
The Style Expert agent will maintain both files automatically:
- `*add-item` - Adds to both index and items
- `*bulk-import` - Processes multiple items at once
- `*update-item` - Updates both files
- `*remove-item` - Removes from both files

### 3. Manual Editing (Advanced)
If editing JSON manually:
1. Add full item to `wardrobe_items.json` items array
2. Add lightweight entry to `wardrobe_index.json` index array
3. Ensure IDs match between both files
4. Keep indexed fields (name, type, category, primaryColor, formality, seasons, tags) consistent

## File Maintenance

### Keep in Sync
The index and items files must stay synchronized. The Style Expert agent handles this automatically.

**If manually editing:**
- Add item to items → Also add to index
- Update indexed field → Update in both files
- Remove item → Remove from both files

### Indexed Fields (must match in both files)
- id
- name
- type
- category
- primaryColor (from metadata.colors.primary)
- formality (from metadata.formality)
- seasons (from context.seasons)
- tags

### Validation
Occasionally verify sync:
```bash
# All IDs in index should exist in items
# Count should match
jq '.index | length' wardrobe_index.json
jq '.items | length' wardrobe_items.json
```

## Benefits

✅ **Efficient filtering** - Find items without loading everything
✅ **Scalable** - Works with 10 items or 1000 items
✅ **Context-aware** - Only load what you need
✅ **Fast queries** - Index is always quick to scan
✅ **Maintainable** - Agent handles sync automatically

## Migration from Individual Files

If you have individual `item_*.json` files:

1. Collect all items into `wardrobe_items.json`:
```json
{
  "items": [
    /* paste all individual item objects here */
  ]
}
```

2. Generate index from items (or use agent's bulk-import)

3. Archive individual files (keep as backup initially)
