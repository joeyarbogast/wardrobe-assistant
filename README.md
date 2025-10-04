# StyleBot - AI-Powered Personal Wardrobe Stylist

> Your personal styling assistant powered by Claude AI. Get outfit recommendations based on occasion, weather, and your unique wardrobe—no fashion experience required.

## What is StyleBot?

StyleBot is a Claude Code agent that acts as your personal stylist. It learns your wardrobe, understands context (weather, occasion, formality), and recommends outfits that make you look and feel confident. Over time, it learns from your feedback to provide increasingly personalized recommendations.

### Key Features

- **Smart Outfit Recommendations** - Get 2-3 outfit options tailored to your specific occasion and weather
- **Context-Aware** - Considers formality, season, temperature, activities, and time of day
- **Visual Analysis** - Claude analyzes clothing images to understand colors, patterns, materials, and style
- **Learning System** - Improves recommendations based on your ratings and feedback
- **Wardrobe Management** - Track what you own, wear counts, and when items were last worn
- **HTML Visualizations** - Beautiful outfit previews you can save and reference
- **Privacy-First** - All data stays in your private repository

### Perfect For

- Men who want to dress better but lack styling experience
- Anyone with "what should I wear?" decision fatigue
- People who want to maximize their existing wardrobe
- Those who feel uncertain about dressing appropriately for occasions

## Quick Start

### Prerequisites

- **Claude Pro or Team subscription** (required for Claude Code)
- **Git** installed on your machine
- **VS Code** with Claude Code extension (or Claude Code CLI)
- Basic familiarity with command line

### Setup (5 minutes)

1. **Fork or clone this template repository**
   ```bash
   git clone https://github.com/yourusername/wardrobe-picker-template.git my-wardrobe
   cd my-wardrobe
   ```

2. **Make it private** (recommended - contains your personal data)
   - If forked: Go to repository Settings → Change visibility to Private
   - If using locally: This is already private

3. **Initialize your wardrobe data**
   ```bash
   # From template/ directory
   cp templates/wardrobe/wardrobe_index.template.json data/wardrobe/wardrobe_index.json
   cp templates/wardrobe/wardrobe_items.template.json data/wardrobe/wardrobe_items.json
   ```

4. **Start StyleBot**
   ```bash
   # From template/ directory
   claude-code
   ```
   Then type: `@style-expert`

5. **Add your first item**
   ```
   *add-item
   ```
   Follow the prompts to add a clothing item (you'll need an image)

See [SETUP.md](SETUP.md) for detailed setup instructions.

## How It Works

### The Workflow Loop

```
1. Add Wardrobe Items
   ↓
2. Get Outfit Recommendations
   ↓
3. Wear the Outfit & Take Photo
   ↓
4. Provide Feedback & Ratings
   ↓
5. StyleBot Learns Your Preferences
   ↓
(repeat from step 2 with smarter recommendations)
```

### Architecture

StyleBot uses an efficient **index-based architecture** that scales to hundreds of wardrobe items:

- **Wardrobe Index** (~100 bytes/item) - Quick filtering by color, type, season, formality
- **Wardrobe Items** (~1.5KB/item) - Full metadata loaded only when needed
- **Recommendations** (JSON + HTML) - Structured data + visual previews
- **Feedback** (JSON) - Ratings and learning data

This means even with 500 wardrobe items, StyleBot only loads ~20-40KB for most queries instead of 750KB.

## Usage Examples

### Get Outfit Recommendation
```
*recommend-outfit

StyleBot: What's the occasion?
You: Business casual work meeting, then dinner with friends

StyleBot: What's the weather like?
You: 65-75°F, partly cloudy

StyleBot: [loads index, filters, builds outfit]
Here are 3 outfit options for you...
```

### Explore Ideas
```
*what-if

You: What if I pair my navy blazer with khaki chinos and brown boots?

StyleBot: [analyzes combination]
Great combination! Here's why this works:
- Navy and khaki are complementary neutrals
- Formality level: 7/10 (smart casual to business casual)
- Brown boots tie in the warm tones...
```

### Rate an Outfit
```
*rate-outfit

StyleBot: Which recommendation would you like to rate?
You: rec_20251004_001

StyleBot: Did you wear it as recommended or make changes?
You: Swapped the shoes for sneakers

StyleBot: How would you rate it overall? (1-5)
You: 5 - got compliments!

StyleBot: [saves feedback, updates item wear counts]
Excellent! I'll remember that the sneaker swap worked well for this formality level.
```

## Available Commands

All commands use the `*` prefix when talking to StyleBot:

- `*help` - Show all available commands
- `*add-item` - Add single clothing item with AI analysis
- `*bulk-import` - Import multiple items from a directory
- `*recommend-outfit` - Get outfit recommendations for an occasion
- `*what-if` - Test outfit combinations without saving
- `*rate-outfit` - Provide feedback on worn outfits
- `*show-wardrobe` - View your wardrobe with filtering options
- `*update-item` - Modify item metadata
- `*remove-item` - Delete item from wardrobe
- `*exit` - Exit StyleBot agent

See [USAGE.md](USAGE.md) for detailed command documentation and examples.

## Project Structure

```
template/
├── .claude/
│   └── agents/
│       └── style-expert-agent.md    # StyleBot agent definition
├── data/
│   ├── wardrobe/
│   │   ├── wardrobe_index.json      # Lightweight item index
│   │   ├── wardrobe_items.json      # Full item details
│   │   └── README.md                # Index architecture docs
│   ├── recommendations/
│   │   └── *.json                   # Saved outfit recommendations
│   └── feedback/
│       └── *.json                   # Feedback and ratings
├── images/                          # Your clothing photos
├── output/
│   └── *.html                       # Generated HTML visualizations
├── templates/
│   └── recommendation.html          # HTML template for outfits
├── README.md                        # This file
├── SETUP.md                         # Detailed setup guide
└── USAGE.md                         # Command reference & workflows
```

## Privacy & Data

### Your Data Stays Private

- This is a **template repository** - fork it to your own private repo
- All wardrobe data, photos, and recommendations stay on your machine
- Claude processes images and text but doesn't store your personal data
- Recommendations are generated on-demand, not stored by Anthropic

### What Gets Committed to Git

✅ **Should commit:**
- Wardrobe metadata (wardrobe_index.json, wardrobe_items.json)
- Recommendations (JSON files)
- Feedback data
- Generated HTML files (optional)

❌ **Should NOT commit (add to .gitignore):**
- Personal photos (images/ directory) - optional, up to you
- Temporary files

### Recommended .gitignore
```
# Optional: exclude photos if they're too personal
images/

# Temporary files
*.tmp
.DS_Store
```

## Learning & Improvement

StyleBot gets smarter over time by:

1. **Tracking Wear Patterns** - Notes which items you actually wear
2. **Learning from Ratings** - High-rated outfits inform future recommendations
3. **Understanding Modifications** - When you swap items, it learns your preferences
4. **Avoiding Mistakes** - Low-rated combinations won't be repeated
5. **Identifying Favorites** - Items that get compliments or high ratings are prioritized

## Requirements

### Required
- **Claude Pro or Team subscription** ($20/month) - Needed for Claude Code access
- **Git** - For version control
- **Claude Code** - Available as VS Code extension or CLI
- **Image files** of your clothing (PNG, JPG, or screenshots from online shopping)

### Optional
- **Web browser** - For viewing HTML outfit visualizations
- **Smartphone** - For taking photos of worn outfits (feedback loop)

## Limitations

- **Image quality matters** - Clear, well-lit photos work best for AI analysis
- **Context window** - Very large wardrobes (1000+ items) may need optimization
- **Color accuracy** - Claude does its best but screen colors may vary from real life
- **Personal taste** - StyleBot learns over time but starts with general fashion rules
- **Photo storage** - You manage your own image library (not automated)

## Roadmap / Future Ideas

- [ ] Integration with weather APIs for automatic temperature lookup
- [ ] Calendar integration for automatic occasion detection
- [ ] Outfit photo stitching (visual preview before trying on)
- [ ] Seasonal wardrobe analysis (gaps, suggestions)
- [ ] Color palette extraction and coordination rules
- [ ] Packing list generator for trips
- [ ] Donation suggestions (items rarely worn)

## Contributing

This is a personal-use template, but improvements are welcome!

- Found a bug? Open an issue
- Have a feature idea? Start a discussion
- Want to improve documentation? Submit a PR

## License

MIT License - Use freely, modify as needed, make it your own.

## Credits

Built with:
- [Claude](https://claude.ai) by Anthropic
- [Claude Code](https://docs.claude.com/claude-code) for agent workflows
- Inspired by personal styling services and fashion recommendation systems

---

**Ready to never worry about "what should I wear?" again?**

See [SETUP.md](SETUP.md) to get started in 5 minutes.
