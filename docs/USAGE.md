# StyleBot Usage Guide

Complete reference for all StyleBot commands, workflows, and best practices.

## Table of Contents

- [Getting Started](#getting-started)
- [Command Reference](#command-reference)
- [Common Workflows](#common-workflows)
- [Best Practices](#best-practices)
- [Tips & Tricks](#tips--tricks)

---

## Getting Started

### Activating StyleBot

1. **Open Claude Code** in your template directory
2. **Type:** `@style-expert`
3. **StyleBot greets you** and displays available commands

### Deactivating StyleBot

Type: `*exit` to return to normal Claude mode

### Getting Help Anytime

Type: `*help` to see the command list

---

## Command Reference

All commands use the `*` prefix. Commands are case-insensitive.

### Wardrobe Management

#### `*add-item`

Add a single clothing item to your wardrobe with AI-powered analysis.

**Usage:**
```
*add-item
```

**Workflow:**
1. StyleBot asks for image path
2. Provide path: `images/wardrobe/Brand_Color_Type.png`
3. Claude analyzes image using vision AI
4. Reviews auto-populated metadata with you:
   - Brand, type, category
   - Colors (primary, secondary, accent)
   - Patterns, material, fit
   - Formality level (1-10)
   - Seasons, occasions
   - Style tags
5. You confirm or make adjustments
6. Item added to both `wardrobe_index.json` and `wardrobe_items.json`

**Example:**
```
You: *add-item

StyleBot: Please provide the image path for the clothing item.

You: images/wardrobe/Bonobos_Navy_Chinos.png

StyleBot: [analyzes image]
I've analyzed the image. Here's what I found:

Name: Navy Weekday Warrior Chinos
Brand: Bonobos
Type: Bottoms
Category: Chinos
Primary Color: Navy Blue
Formality: 6 (Smart Casual to Business Casual)
Seasons: Spring, Summer, Fall
Material: Cotton blend with stretch
Fit: Tailored

Does this look correct? (yes/no/adjust)

You: yes

StyleBot: ✓ Added item_20251005_001 to wardrobe
```

**Tips:**
- Use clear, well-lit images
- Screenshots from shopping sites work great
- Name images descriptively (helps AI analysis)

---

#### `*bulk-import`

Import multiple items at once from a directory.

**Usage:**
```
*bulk-import
```

**Workflow:**
1. StyleBot asks for directory path
2. Provide: `images/wardrobe/new-items/`
3. StyleBot processes each image
4. Shows progress as items are analyzed
5. Presents summary for review
6. All items added to wardrobe at once

**Example:**
```
You: *bulk-import

StyleBot: Which directory contains the images to import?

You: images/wardrobe/stitch-fix-august/

StyleBot: Found 8 images. Processing...
[1/8] Analyzing Bonobos_Navy_Chinos.png... ✓
[2/8] Analyzing JCrew_White_OCBD.png... ✓
...
[8/8] Analyzing Clarks_Brown_Boots.png... ✓

Successfully imported 8 items!
- 3 tops
- 2 bottoms
- 2 shoes
- 1 outerwear

Review? (yes/details/edit)
```

**Tips:**
- Best for initial wardrobe setup or seasonal hauls
- Organize images in folders by type first
- Review batch before committing

---

#### `*show-wardrobe`

View your wardrobe with optional filtering and sorting.

**Usage:**
```
*show-wardrobe
```

**Workflow:**
1. StyleBot asks for filter preferences
2. Options: all, by type, by category, by tag, by formality, by season
3. Displays matching items with key metadata
4. Can request detailed view for specific items

**Example:**
```
You: *show-wardrobe

StyleBot: How would you like to view your wardrobe?
1. All items
2. Filter by type (tops, bottoms, etc.)
3. Filter by category
4. Filter by tag
5. Filter by formality level
6. Filter by season

You: 2

StyleBot: Which type?
- Tops (15 items)
- Bottoms (8 items)
- Outerwear (5 items)
- Shoes (6 items)
- Accessories (3 items)

You: tops

StyleBot: Tops (15 items)

🔵 Navy Oxford Button-Down (item_001)
   Formality: 6 | Seasons: All | Tags: classic, versatile

⚪ White Performance Polo (item_004)
   Formality: 5 | Seasons: Spring, Summer | Tags: athletic, casual

[... more items ...]

View details for any item? (enter ID or 'done')
```

**Filters:**
- **By type:** tops, bottoms, outerwear, shoes, accessories
- **By formality:** 1-10 scale
- **By season:** spring, summer, fall, winter
- **By tag:** casual, professional, athletic, etc.

---

#### `*update-item`

Modify metadata for an existing item.

**Usage:**
```
*update-item
```

**Workflow:**
1. Search for item by ID or name
2. StyleBot displays current metadata
3. You specify which fields to update
4. Updates both index and items files
5. Timestamp updated automatically

**Example:**
```
You: *update-item

StyleBot: Which item? (ID or search by name)

You: navy chinos

StyleBot: Found 2 matches:
1. Navy Weekday Warrior Chinos (item_001)
2. Navy Performance Chinos (item_015)

You: 1

StyleBot: [shows current metadata]
Which fields would you like to update?

You: Add "favorite" tag and update seasons to include winter

StyleBot: ✓ Updated item_001
- Added tag: favorite
- Seasons: Spring, Summer, Fall, Winter
```

---

#### `*remove-item`

Delete an item from your wardrobe.

**Usage:**
```
*remove-item
```

**Workflow:**
1. Search by ID or name
2. StyleBot displays item for confirmation
3. Confirm deletion
4. Removes from both index and items files

**Example:**
```
You: *remove-item

StyleBot: Which item? (ID or search)

You: old gray tshirt

StyleBot: Found: Gray Basic Crew Neck Tee (item_032)
[displays details]

Are you sure you want to remove this item? (yes/no)

You: yes

StyleBot: ✓ Removed item_032 from wardrobe
```

---

### Outfit Recommendations

#### `*recommend-outfit`

Get AI-powered outfit recommendations based on context.

**Usage:**
```
*recommend-outfit
```

**Workflow:**
1. StyleBot gathers context:
   - Occasion/activity
   - Weather (temperature, conditions)
   - Duration
   - Special considerations
2. Loads wardrobe index and filters by criteria
3. Loads full details for candidate items
4. Builds 2-3 outfit options
5. Presents with reasoning and alternatives
6. Saves recommendation as JSON
7. Optionally generates HTML visualization

**Example:**
```
You: *recommend-outfit

StyleBot: What's the occasion or activity?

You: Business casual office meeting, then casual dinner with friends

StyleBot: What's the weather like?

You: 60-72°F, partly cloudy

StyleBot: How long will you be out?

You: 9am to 9pm

StyleBot: Any special considerations? (comfort, specific items, colors to avoid)

You: Want to look professional but not overdressed for dinner

StyleBot: [analyzes wardrobe]

I have 3 outfit recommendations for you:

━━━━━━━━━━━━━━━━━━━━━
OPTION 1: Smart Casual Bridge ⭐ RECOMMENDED
━━━━━━━━━━━━━━━━━━━━━

👔 Navy Weekday Warrior Chinos (item_001)
   WHY: Versatile formality (6/10) bridges business casual meeting
   and dinner. Navy is professional yet approachable.

👕 Light Blue Oxford Button-Down (item_003)
   WHY: Classic business casual staple. Light blue adds warmth
   without being too formal. Can roll sleeves for dinner.

👞 Brown Leather Loafers (item_018)
   WHY: Professional enough for meeting, comfortable for all-day wear,
   casual enough for dinner.

🧥 [Optional] Charcoal Blazer (item_007)
   WHY: Elevates look for meeting, easily removable for dinner.

FORMALITY: 6.5/10 (perfect for your range)
COLOR STRATEGY: Navy + light blue + brown (classic, complementary)
WEATHER: Appropriate for 60-72°F with optional layer

━━━━━━━━━━━━━━━━━━━━━
OPTION 2: Modern Professional
[... details ...]

━━━━━━━━━━━━━━━━━━━━━
OPTION 3: Relaxed Smart Casual
[... details ...]

Would you like me to:
1. Generate HTML visualization
2. Explore variations
3. Save and exit

You: 1

StyleBot: ✓ Saved as rec_20251005_001.json
✓ Generated output/rec_20251005_001.html
Open in browser? (yes/no)
```

**Context Questions:**
- **Occasion:** Work, casual, date, interview, wedding, etc.
- **Weather:** Temperature range and conditions
- **Duration:** How long you'll be out
- **Activities:** Multiple activities (hiking then dinner)
- **Special needs:** Comfort, specific colors, items to include/avoid

**Output:**
- 2-3 ranked outfit options
- Reasoning for each item selected
- Color coordination strategy
- Formality assessment
- Alternative suggestions
- Saved JSON recommendation
- Optional HTML visualization

---

#### `*what-if`

Explore outfit combinations interactively without saving.

**Usage:**
```
*what-if
```

**Workflow:**
1. You propose a combination (by item ID or description)
2. StyleBot analyzes the pairing
3. Provides styling feedback
4. Suggests improvements
5. Conversation-based exploration (nothing saved)

**Example:**
```
You: *what-if

StyleBot: What combination would you like to try?

You: Navy blazer with gray chinos and white sneakers

StyleBot: Let me analyze this combination...

✓ Color Coordination: Excellent
- Navy + gray is a classic neutral pairing
- White sneakers add modern, clean accent

✓ Formality: Mixed (6/10 top + 6/10 bottom + 3/10 shoes = 5/10 overall)
- Blazer and chinos are smart casual (6-7/10)
- White sneakers bring it down to casual (3-4/10)
- RESULT: Relaxed smart casual (5/10)

✓ Style: Modern, slightly dressed-down professional

WORKS WELL FOR:
- Casual Friday office
- Weekend brunch
- Informal client meeting
- Date night (casual venue)

ALTERNATIVES TO CONSIDER:
- Swap sneakers for loafers → Elevates to true smart casual (6.5/10)
- Swap blazer for sweater → More cohesive casual look (4/10)
- Add brown belt → Ties in earth tones if using tan/brown sneakers

Want to try another combination?
```

**Use Cases:**
- Test ideas before committing
- Learn about color coordination
- Understand formality matching
- Experiment with your wardrobe

---

### Feedback & Learning

#### `*rate-outfit`

Provide feedback on outfits you've worn to improve future recommendations.

**Usage:**
```
*rate-outfit
```

**Workflow:**
1. Select recent recommendation or provide ID
2. Confirm if worn as recommended or modified
3. Provide ratings (overall, comfort, appropriateness, confidence)
4. Share what worked well and what didn't
5. Add tags (got-compliments, too-casual, felt-great, etc.)
6. Optionally attach photo of worn outfit
7. StyleBot saves feedback and updates wear counts

**Example:**
```
You: *rate-outfit

StyleBot: Which recommendation? (recent or provide ID)

Recent recommendations:
1. rec_20251005_001 - Business meeting & dinner
2. rec_20251004_003 - Casual weekend
3. rec_20251003_001 - Date night

You: 1

StyleBot: Did you wear the outfit as recommended, or make changes?

You: Swapped the brown loafers for white sneakers

StyleBot: Ah, interesting! Going more casual.

Rate the outfit overall (1-5): ⭐⭐⭐⭐⭐

You: 5

StyleBot: Comfort level (1-5):

You: 5

StyleBot: Appropriateness for occasion (1-5):

You: 4

StyleBot: Confidence/how you felt (1-5):

You: 5

StyleBot: What worked well?

You: The navy chinos and light blue shirt were perfect. Got compliments!
Sneakers made me more comfortable for the long day.

StyleBot: What didn't work or could improve?

You: The blazer was too warm. Didn't need it.

StyleBot: Any tags? (got-compliments, comfortable, too-formal, etc.)

You: got-compliments, comfortable, versatile

StyleBot: Photo of worn outfit? (path or 'skip')

You: skip

StyleBot: ✓ Feedback saved as feedback_20251005_001.json

KEY LEARNINGS:
✓ Navy chinos + light blue oxford is a winning combination
✓ You prefer sneakers over loafers for all-day comfort
✓ Blazer was unnecessary for this formality level
✓ Items worn: Updated wear counts for item_001, item_003, item_022

I'll remember these preferences for future recommendations!
```

**Rating Scales:**
- **Overall:** 1-5 stars (general satisfaction)
- **Comfort:** How physically comfortable
- **Appropriateness:** How well it matched the occasion
- **Confidence:** How you felt wearing it

**Common Tags:**
- `got-compliments` - Others noticed positively
- `comfortable` - Felt good all day
- `too-formal` - Overdressed
- `too-casual` - Underdressed
- `favorite` - Want to repeat
- `avoid` - Don't recommend again
- `versatile` - Worked for multiple settings

---

## Common Workflows

### Workflow 1: Initial Wardrobe Setup

**Goal:** Get your wardrobe into the system

1. **Gather images** of your clothing
   - Take photos or use screenshots from shopping sites
   - Organize into folders: tops/, bottoms/, shoes/, etc.

2. **Bulk import by category**
   ```
   *bulk-import
   > images/wardrobe/tops/
   ```

3. **Repeat for each category**

4. **Verify with show-wardrobe**
   ```
   *show-wardrobe
   > all
   ```

5. **Clean up example items**
   ```
   *remove-item
   > item_20251004_001
   ```

**Time estimate:** 30-60 minutes for 50 items

---

### Workflow 2: Daily Outfit Selection

**Goal:** Get dressed confidently for the day

1. **Activate StyleBot**
   ```
   @style-expert
   ```

2. **Request recommendation**
   ```
   *recommend-outfit
   ```

3. **Provide context**
   - Where you're going
   - Weather conditions
   - Any special considerations

4. **Review options**
   - 2-3 outfit recommendations
   - Read reasoning

5. **Choose and wear**
   - Pick your favorite option
   - Or mix elements from multiple options

6. **Optional: Generate HTML to save/print**

**Time estimate:** 3-5 minutes

---

### Workflow 3: Weekend Wardrobe Exploration

**Goal:** Learn about your wardrobe and discover new combinations

1. **Browse your wardrobe**
   ```
   *show-wardrobe
   > Filter by: tops
   ```

2. **Experiment with combinations**
   ```
   *what-if
   > Blue shirt with khaki chinos and brown boots
   ```

3. **Try different pairings**
   ```
   *what-if
   > Same outfit but swap boots for sneakers
   ```

4. **Learn styling principles**
   - StyleBot explains why things work or don't
   - Build your fashion knowledge

**Time estimate:** 15-30 minutes

---

### Workflow 4: Post-Wear Feedback Loop

**Goal:** Improve future recommendations

1. **After wearing an outfit, provide feedback**
   ```
   *rate-outfit
   > rec_20251005_001
   ```

2. **Rate honestly**
   - What worked, what didn't
   - Comfort, appropriateness, confidence

3. **Add specific notes**
   - "Got compliments on the color combo"
   - "Shoes were uncomfortable after 2 hours"

4. **Attach photo (optional)**
   - Take full-body mirror selfie
   - Save to `images/worn-outfits/`

5. **StyleBot learns**
   - Updates item wear counts
   - Notes successful combinations
   - Avoids poor matches in future

**Frequency:** After each significant outfit (1-3x per week)

---

### Workflow 5: Seasonal Wardrobe Update

**Goal:** Add new items and refresh for new season

1. **Import new purchases**
   ```
   *bulk-import
   > images/wardrobe/fall-2024/
   ```

2. **Update seasonal metadata**
   ```
   *update-item
   > [lightweight jacket]
   > Add seasons: fall, winter
   ```

3. **Review seasonal wardrobe**
   ```
   *show-wardrobe
   > Filter by season: fall
   ```

4. **Get recommendations for new season**
   ```
   *recommend-outfit
   > Casual fall weekend
   ```

**Frequency:** 2-4 times per year

---

## Best Practices

### Image Management

✅ **Do:**
- Use clear, well-lit photos
- Screenshot product pages (shows item flat/clean)
- Name files descriptively: `Brand_Color_Type.png`
- Organize by category (tops/, bottoms/, etc.)
- Keep image sizes reasonable (< 5MB)

❌ **Don't:**
- Use blurry or dark photos
- Mix multiple items in one image
- Use generic filenames (IMG_001.jpg)
- Store in random directories

### Metadata Quality

✅ **Do:**
- Review AI-generated metadata carefully
- Add personal notes ("runs small", "very warm")
- Use consistent tag vocabulary
- Update formality based on your perception
- Keep seasons realistic for your climate

❌ **Don't:**
- Accept AI suggestions blindly
- Skip the review step
- Use random/inconsistent tags
- Ignore obvious errors

### Recommendation Workflow

✅ **Do:**
- Be specific about context (occasion, weather, duration)
- Mention special considerations upfront
- Review all options before deciding
- Generate HTML for important events (save for reference)
- Modify recommendations to your preference

❌ **Don't:**
- Give vague context ("going out")
- Ignore weather/formality requirements
- Always take first recommendation
- Feel locked into suggestions

### Feedback Loop

✅ **Do:**
- Rate outfits within a few days (while fresh)
- Be honest about what didn't work
- Note modifications you made
- Provide specific details in notes
- Take photos when possible

❌ **Don't:**
- Rate everything 5 stars (StyleBot can't learn)
- Wait weeks to provide feedback (you'll forget)
- Skip feedback for "unremarkable" outfits (data is valuable)
- Only rate positive experiences

### Git & Version Control

✅ **Do:**
- Commit after bulk changes (imports, updates)
- Use descriptive commit messages
- Review changes before committing
- Keep backup of data files

❌ **Don't:**
- Commit after every single item add
- Use vague messages ("update")
- Ignore git entirely (lose change history)

---

## Tips & Tricks

### Power User Shortcuts

**Quick Wardrobe Stats:**
```
*show-wardrobe
> all, sorted by wear count

See which items you actually wear vs. closet orphans
```

**Formality Finder:**
```
*show-wardrobe
> Filter by formality: 7-8

Quickly see all business casual options
```

**Seasonal Prep:**
```
*show-wardrobe
> Filter by season: summer
> Then: Filter by tag: lightweight

Find hot-weather appropriate items
```

### Recommendation Hacks

**Multi-Activity Days:**
Be explicit about transitions:
```
*recommend-outfit
> Morning: Job interview (business formal)
> Evening: Drinks with friends (smart casual)
> Need outfit that transitions or easy items to swap
```

**Special Constraints:**
```
*recommend-outfit
> Casual dinner date
> Must include: navy chinos (just cleaned)
> Avoid: anything white (eating pasta)
> Formality: 5-6
```

**Weather Uncertainty:**
```
*recommend-outfit
> Outdoor event
> 60-75°F but might rain
> Need: layerable outfit with backup plan
```

### Learning Faster

**Study StyleBot's Reasoning:**
- Read the "WHY" for each item selection
- Note color coordination strategies
- Understand formality calculations
- Learn pattern mixing rules

**Experiment with What-If:**
```
*what-if
> [your idea]

*what-if
> Same thing but swap [item X] for [item Y]

Compare StyleBot's analysis of variations
```

**Track Your Patterns:**
- Notice which items get high ratings repeatedly
- Identify combinations that get compliments
- See which pieces you never wear
- Use this data for future shopping

### Maintenance

**Monthly Review:**
1. Check items with 0 wear count (consider donating)
2. Update metadata based on actual use
3. Add tags based on feedback patterns
4. Remove items you've donated/sold

**Seasonal Audit:**
1. Review upcoming season's wardrobe
2. Identify gaps (missing formality levels, colors)
3. Plan purchases to fill gaps
4. Update any seasonal metadata

**Data Hygiene:**
1. Verify index and items files are in sync
2. Clean up unused image files
3. Archive old recommendations (move to `archive/`)
4. Backup your data files

---

## Advanced Features

### HTML Customization

Edit `templates/recommendation.html` to customize the visual output:
- Change colors/fonts
- Add your branding
- Modify layout
- Include additional metadata

### Scripting Integration

**Export wardrobe stats:**
```bash
jq '.index | group_by(.type) | map({type: .[0].type, count: length})' data/wardrobe/wardrobe_index.json
```

**Find unworn items:**
```bash
jq '.items[] | select(.tracking.wearCount == 0) | .name' data/wardrobe/wardrobe_items.json
```

**Most worn items:**
```bash
jq '.items | sort_by(-.tracking.wearCount) | .[0:5] | .[] | {name, wearCount: .tracking.wearCount}' data/wardrobe/wardrobe_items.json
```

### Backup Strategy

**Daily (automatic via git):**
```bash
# Add to cron or scheduled task
cd ~/my-wardrobe/template && \
git add . && \
git commit -m "Daily backup $(date)" && \
git push
```

**Monthly (full backup):**
```bash
tar -czf wardrobe-backup-$(date +%Y%m).tar.gz template/
```

---

## Frequently Asked Questions

**Q: How many items should I start with?**
A: Start with 10-20 frequently worn items. Build from there. No need to add every sock and t-shirt immediately.

**Q: Should I add seasonal items I'm not currently wearing?**
A: Yes! Add them when you have time, even if out of season. Then they're ready when weather changes.

**Q: Can I edit the JSON files directly?**
A: Yes, but use `*update-item` when possible. Direct editing risks breaking the index/items sync.

**Q: What if StyleBot recommends something I don't like?**
A: Perfect! Try `*what-if` to explore alternatives, or modify the recommendation and rate it with your changes. StyleBot learns from this.

**Q: How often should I provide feedback?**
A: Rate at least weekly outfits. The more feedback, the better StyleBot learns your preferences.

**Q: Can I use this for formal events (weddings, black tie)?**
A: Yes! Add your formal wear to the wardrobe. StyleBot handles formality levels 1-10.

**Q: What about accessories (watches, jewelry, bags)?**
A: Add them as wardrobe items! Use type: "accessories" and appropriate formality levels.

---

**Ready to master your wardrobe?**

Start with `@style-expert` and explore the commands!
