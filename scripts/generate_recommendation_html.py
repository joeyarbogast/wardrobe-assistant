#!/usr/bin/env python3
"""
Recommendation HTML Generator
Converts recommendation JSON files to beautiful HTML visualizations.

Usage:
    python scripts/generate_recommendation_html.py rec_20251005_001
    python scripts/generate_recommendation_html.py rec_20251005_001 --output custom_name.html
"""

import json
import argparse
import sys
from pathlib import Path

# Set base path to project root
BASE_PATH = Path(__file__).parent.parent
RECOMMENDATIONS_DIR = BASE_PATH / "data" / "recommendations"
TEMPLATE_PATH = BASE_PATH / "templates" / "recommendations" / "recommendation.html"
WARDROBE_ITEMS = BASE_PATH / "data" / "wardrobe" / "wardrobe_items.json"


# Color mapping for visualization
COLOR_MAP = {
    'light blue': '#87CEEB',
    'dark grey': '#4A5568',
    'dark gray': '#4A5568',
    'tan': '#D2B48C',
    'brown': '#8B4513',
    'navy': '#001f3f',
    'navy blue': '#001f3f',
    'grey': '#718096',
    'gray': '#718096',
    'black': '#000000',
    'white': '#FFFFFF',
    'olive green': '#556B2F',
    'olive': '#556B2F',
    'beige': '#F5F5DC',
    'burgundy': '#800020',
    'red': '#DC143C',
    'blue': '#4169E1',
    'indigo': '#4B0082',
    'light purple': '#D8BFD8',
    'burnt orange': '#CC5500',
    'yellow': '#FFD700',
    'teal blue': '#008080',
    'khaki': '#C3B091'
}


def load_recommendation(rec_id):
    """Load recommendation JSON file."""
    rec_path = RECOMMENDATIONS_DIR / f"{rec_id}.json"
    if not rec_path.exists():
        print(f"Error: Recommendation file not found: {rec_path}", file=sys.stderr)
        sys.exit(1)

    with open(rec_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_template():
    """Load HTML template."""
    if not TEMPLATE_PATH.exists():
        print(f"Error: Template file not found: {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def get_image_paths():
    """Load image paths from wardrobe items."""
    with open(WARDROBE_ITEMS, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create mapping of item_id -> imagePath
    image_map = {}
    for item in data['items']:
        image_map[item['id']] = item.get('imagePath', '')

    return image_map


def build_context_html(context):
    """Build context bar HTML."""
    occasion = context.get('occasion', 'Occasion')
    time = context.get('timeOfDay', 'day')
    temp = context.get('weather', {}).get('temperature', '?')
    unit = context.get('weather', {}).get('unit', 'F')

    # Determine icon based on occasion/context
    occasion_lower = occasion.lower()
    if 'dinner' in occasion_lower or 'restaurant' in occasion_lower:
        icon = '🍝'
    elif 'business' in occasion_lower or 'meeting' in occasion_lower:
        icon = '💼'
    elif 'date' in occasion_lower:
        icon = '💕'
    elif 'casual' in occasion_lower or 'weekend' in occasion_lower:
        icon = '👕'
    else:
        icon = '📅'

    context_html = f'''
<div class="context-item">
    <span class="icon">{icon}</span>
    <span class="label">{occasion.title()}</span>
</div>
<div class="context-item">
    <span class="icon">🌡️</span>
    <span class="label">{temp}°{unit[0].upper()}</span>
</div>
<div class="context-item">
    <span class="icon">🕐</span>
    <span class="label">{time.title()}</span>
</div>
'''

    # Add mood if present
    mood = context.get('mood')
    if mood:
        context_html += f'''
<div class="context-item">
    <span class="icon">😊</span>
    <span class="label">{mood.title()}</span>
</div>
'''

    return context_html


def build_outfit_section(outfit, outfit_name, outfit_number, image_map):
    """Build HTML for a single outfit option."""
    items_html = ''

    for item in outfit['items']:
        img_path = image_map.get(item['id'], '')
        rel_path = f"../../{img_path}" if img_path else ''

        img_html = f'<img src="{rel_path}" alt="{item["name"]}">' if rel_path else '<span class="item-icon">👔</span>'

        items_html += f'''
        <div class="item-card">
            <div class="item-badge">{item['role']}</div>
            <div class="item-image">{img_html}</div>
            <div class="item-name">{item['name']}</div>
            <div class="item-meta">{item['category'].title()}</div>
            <div class="item-reason">{item['reason']}</div>
        </div>
        '''

    # Build color palette
    colors_html = ''
    all_colors = outfit.get('dominantColors', []) + outfit.get('accentColors', [])
    for color in all_colors:
        color_code = COLOR_MAP.get(color.lower(), '#CCCCCC')
        colors_html += f'''
        <div class="color-swatch">
            <div class="color-circle" style="background-color: {color_code};"></div>
            <div class="color-name">{color.title()}</div>
        </div>
        '''

    # Icon for each option
    icons = ['🌟', '✨', '💫']
    icon = icons[outfit_number - 1] if outfit_number <= 3 else '👔'

    outfit_section = f'''
    <div class="section" style="margin-bottom: 60px; padding-bottom: 40px; border-bottom: 2px solid #e2e8f0;">
        <h2 class="section-title" style="color: #667eea;">{icon} Option {outfit_number}: {outfit_name}</h2>
        <div class="outfit-grid">
            {items_html}
        </div>
        <div class="stats-bar">
            <div class="stat">
                <div class="stat-value">{outfit.get('totalFormality', 'N/A')}</div>
                <div class="stat-label">Formality</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(outfit['items'])}</div>
                <div class="stat-label">Pieces</div>
            </div>
        </div>
        <div style="margin-top: 20px;">
            <h3 style="color: #2d3748; margin-bottom: 10px;">Color Palette</h3>
            <div class="color-palette">{colors_html}</div>
        </div>
    </div>
    '''

    return outfit_section


def build_all_outfits_html(rec, image_map):
    """Build HTML for all outfit options in the recommendation."""
    all_outfits_html = ''

    # Check if recommendation has multiple outfits or single outfit
    outfit = rec.get('outfit', {})

    if 'primary' in outfit:
        # Multiple outfit format
        outfits = [
            (outfit.get('primary', {}), outfit['primary'].get('name', 'Primary'), 1),
            (outfit.get('alternative1', {}), outfit.get('alternative1', {}).get('name', 'Alternative 1'), 2),
            (outfit.get('alternative2', {}), outfit.get('alternative2', {}).get('name', 'Alternative 2'), 3)
        ]

        for outfit_data, name, number in outfits:
            if outfit_data and outfit_data.get('items'):
                all_outfits_html += build_outfit_section(outfit_data, name, number, image_map)

    elif 'items' in outfit:
        # Single outfit format
        all_outfits_html = build_outfit_section(outfit, 'The Outfit', 1, image_map)

    return all_outfits_html


def build_style_notes_html(reasoning):
    """Build style notes list."""
    style_notes = reasoning.get('styleNotes', [])
    notes_html = ''

    for note in style_notes:
        notes_html += f'<li>{note}</li>\n'

    return notes_html


def build_alternatives_html(alternatives):
    """Build alternatives section."""
    variations = alternatives.get('variations', [])
    alts_html = ''

    for alt in variations:
        alts_html += f'''
    <div class="alt-card">
        <h4>{alt.get('type', 'Alternative').title()}</h4>
        <p><strong>{alt.get('description', '')}</strong></p>
        <p>{alt.get('reason', '')}</p>
    </div>
    '''

    return alts_html


def generate_html(rec_id, output_path=None):
    """Generate HTML from recommendation JSON."""
    # Load data
    rec = load_recommendation(rec_id)
    template = load_template()
    image_map = get_image_paths()

    # Build sections
    context = rec.get('context', {})
    occasion = context.get('occasion', 'Outfit Recommendation')

    context_html = build_context_html(context)
    outfits_html = build_all_outfits_html(rec, image_map)
    reasoning = rec.get('reasoning', {})
    style_notes_html = build_style_notes_html(reasoning)
    alternatives_html = build_alternatives_html(rec.get('alternatives', {}))

    # Replace placeholders
    html = template
    html = html.replace('{{HEADER_ICON}}', '👔')
    html = html.replace('{{OCCASION_TITLE}}', occasion.title())
    html = html.replace('{{RECOMMENDATION_ID}}', rec.get('id', rec_id))
    html = html.replace('{{CONTEXT_ITEMS}}', context_html)

    # Replace entire outfit section
    outfit_section_template = '''<div class="section">
                <h2 class="section-title">👔 The Outfit</h2>
                <div class="outfit-grid">
                    {{OUTFIT_ITEMS}}
                </div>

                <div class="stats-bar">
                    <div class="stat">
                        <div class="stat-value">{{FORMALITY_LEVEL}}</div>
                        <div class="stat-label">Formality Level</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{{CONFIDENCE_SCORE}}%</div>
                        <div class="stat-label">Confidence Score</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{{ITEMS_COUNT}}</div>
                        <div class="stat-label">Items Used</div>
                    </div>
                </div>
            </div>'''

    html = html.replace(outfit_section_template, outfits_html)

    # Remove color section (integrated into each outfit)
    color_section = '''<div class="section">
                <h2 class="section-title">🎨 Color Palette</h2>
                <div class="reasoning-box">
                    <div class="color-palette">
                        {{COLOR_SWATCHES}}
                    </div>
                    <p style="margin-top: 20px;"><strong>Color Strategy:</strong> {{COLOR_STRATEGY}}</p>
                </div>
            </div>'''
    html = html.replace(color_section, '')

    # Replace reasoning sections
    html = html.replace('{{OVERALL_REASONING}}', reasoning.get('overall', ''))
    html = html.replace('{{FORMALITY_REASONING}}', reasoning.get('formalityMatch', ''))
    html = html.replace('{{WEATHER_REASONING}}', reasoning.get('weatherAppropriateness', ''))
    html = html.replace('{{OCCASION_REASONING}}', reasoning.get('occasionFit', ''))
    html = html.replace('{{STYLE_NOTES}}', style_notes_html)
    html = html.replace('{{ALTERNATIVES}}', alternatives_html)

    # Write output
    if output_path:
        output_file = Path(output_path)
    else:
        output_file = RECOMMENDATIONS_DIR / f"{rec_id}.html"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML generated: {output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Generate HTML visualization from recommendation JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate HTML for a recommendation (saves to data/recommendations/)
  python scripts/generate_recommendation_html.py rec_20251005_001

  # Generate with custom output path
  python scripts/generate_recommendation_html.py rec_20251005_001 --output my_outfit.html
        """
    )

    parser.add_argument('recommendation_id', help='Recommendation ID (e.g., rec_20251005_001)')
    parser.add_argument('--output', '-o', help='Custom output path (default: data/recommendations/{id}.html)')

    args = parser.parse_args()

    generate_html(args.recommendation_id, args.output)


if __name__ == '__main__':
    main()
