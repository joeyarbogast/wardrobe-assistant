# HTML Template Guide

## recommendation.html Template

This template is used by StyleBot to generate visual outfit recommendations.

### Template Placeholders

Replace these placeholders when generating HTML from recommendation JSON:

#### Header Section
- `{{OCCASION_TITLE}}` - Title for the page (e.g., "Casual Pizza Dinner Outfit")
- `{{HEADER_ICON}}` - Emoji icon for occasion (e.g., "🍕")
- `{{RECOMMENDATION_ID}}` - The recommendation ID (e.g., "rec_20251004_001")

#### Context Bar
- `{{CONTEXT_ITEMS}}` - HTML for context items, format:
  ```html
  <div class="context-item">
      <span class="icon">🍽️</span>
      <span class="label">Casual dinner with brother</span>
  </div>
  ```

#### Outfit Items
- `{{OUTFIT_ITEMS}}` - HTML for each clothing item card, format:
  ```html
  <div class="item-card">
      <div class="item-badge">Top</div>
      <div class="item-image">
          <img src="file:///path/to/image.png" alt="Item Name">
      </div>
      <div class="item-name">Item Name</div>
      <div class="item-meta">Brand • Category</div>
      <div class="item-reason">
          <strong>Why:</strong> Reasoning text here
      </div>
  </div>
  ```
  For optional items, add `optional` class to both card and badge:
  ```html
  <div class="item-card optional">
      <div class="item-badge optional">Optional Layer</div>
      ...
  </div>
  ```

#### Stats Bar
- `{{FORMALITY_LEVEL}}` - Numeric formality (e.g., "3.5")
- `{{CONFIDENCE_SCORE}}` - Percentage without % symbol (e.g., "95")
- `{{ITEMS_COUNT}}` - Number of items (e.g., "5")

#### Color Palette
- `{{COLOR_SWATCHES}}` - HTML for color circles, format:
  ```html
  <div class="color-swatch">
      <div class="color-circle" style="background: #4a5568;"></div>
      <div class="color-name">Dark Gray</div>
  </div>
  ```
- `{{COLOR_STRATEGY}}` - Text explaining color choices

#### Reasoning Sections
- `{{OVERALL_REASONING}}` - Overall outfit assessment
- `{{FORMALITY_REASONING}}` - Formality match explanation
- `{{WEATHER_REASONING}}` - Weather appropriateness
- `{{OCCASION_REASONING}}` - Occasion fit explanation
- `{{STYLE_NOTES}}` - HTML list items, format:
  ```html
  <li>Style tip here</li>
  <li>Another tip</li>
  ```

#### Alternatives
- `{{ALTERNATIVES}}` - HTML for alternative cards, format:
  ```html
  <div class="alt-card">
      <h4>Variation Type</h4>
      <p><strong>Swap:</strong> Description of swap</p>
      <p>Explanation of why this works</p>
  </div>
  ```

### Usage in StyleBot

When generating HTML in the `*recommend-outfit` command:

1. Load this template file
2. Load the recommendation JSON
3. Replace all placeholders with data from the JSON
4. Save to `output/{recommendation_id}.html`
5. Optionally open in browser

### Example Workflow

```yaml
- Load templates/recommendation.html
- Load data/recommendations/{id}.json
- Replace {{RECOMMENDATION_ID}} with json.id
- Replace {{OCCASION_TITLE}} with json.context.occasion
- For each item in json.outfit.items:
    - Generate item card HTML
    - Append to {{OUTFIT_ITEMS}}
- Save to output/{id}.html
```
