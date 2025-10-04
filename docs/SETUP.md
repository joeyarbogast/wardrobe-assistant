# StyleBot Setup Guide

Complete setup instructions to get StyleBot running in under 10 minutes.

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Claude Pro or Team subscription**
  - Required for Claude Code access
  - Sign up at [claude.ai/upgrade](https://claude.ai/upgrade)
  - Cost: $20/month for Pro, custom pricing for Team

- [ ] **Git installed**
  - Check: `git --version`
  - Install: [git-scm.com/downloads](https://git-scm.com/downloads)

- [ ] **Claude Code**
  - **Option A: VS Code Extension** (recommended for beginners)
    - Install VS Code: [code.visualstudio.com](https://code.visualstudio.com)
    - Install Claude Code extension from VS Code marketplace
  - **Option B: CLI** (advanced users)
    - Install via npm: `npm install -g @anthropic-ai/claude-code`
    - Or download from [docs.claude.com/claude-code](https://docs.claude.com/claude-code)

- [ ] **Image files of your clothing**
  - Screenshots from online shopping (PNG, JPG)
  - Photos of items you own
  - Clear, well-lit images work best

## Step 1: Get the Template Repository

### Option A: Fork on GitHub (Recommended)

1. **Fork this repository** to your GitHub account
   - Click "Fork" button on the repository page
   - Choose your account as destination

2. **Make it private** (contains your personal data)
   - Go to your forked repo
   - Settings → General → Change repository visibility
   - Select "Private" → Confirm

3. **Clone to your local machine**
   ```bash
   git clone https://github.com/YOUR_USERNAME/wardrobe-picker-template.git my-wardrobe
   cd my-wardrobe/template
   ```

### Option B: Clone Locally (No GitHub Account)

1. **Clone the template**
   ```bash
   git clone https://github.com/original/wardrobe-picker-template.git my-wardrobe
   cd my-wardrobe/template
   ```

2. **Remove remote and reinitialize** (makes it fully local)
   ```bash
   git remote remove origin
   ```

### Option C: Download ZIP (Simplest)

1. Download ZIP from repository
2. Extract to `my-wardrobe/`
3. Initialize git:
   ```bash
   cd my-wardrobe/template
   git init
   git add .
   git commit -m "Initial wardrobe setup"
   ```

## Step 2: Initialize Wardrobe Data Files

The template includes example template files. You need to create your actual data files:

```bash
# From template/ directory
# Copy templates from templates/ to data/
cp templates/wardrobe/wardrobe_index.template.json data/wardrobe/wardrobe_index.json
cp templates/wardrobe/wardrobe_items.template.json data/wardrobe/wardrobe_items.json
```

**What just happened?**
- `data/wardrobe/wardrobe_index.json` - Your lightweight wardrobe index (starts with 2 example items)
- `data/wardrobe/wardrobe_items.json` - Your full wardrobe details (starts with 2 example items)
- You'll replace these examples with your own items using StyleBot

## Step 3: Set Up Image Storage

Create a directory for your clothing images:

```bash
# From template/ directory
mkdir -p images/wardrobe
```

**Recommended image organization:**
```
images/
├── wardrobe/          # Individual clothing items
│   ├── tops/
│   ├── bottoms/
│   ├── outerwear/
│   ├── shoes/
│   └── accessories/
└── worn-outfits/      # Photos of you wearing complete outfits (optional)
```

**Image naming convention (helps Claude analyze):**
```
BrandName_Color_Type_Details.png

Examples:
- Bonobos_Navy_ButtonDown_ShortSleeve.png
- Levis_Black_Jeans_Slim_511.png
- Nike_White_Sneakers_AirForce1.png
```

## Step 4: Configure Git (Optional but Recommended)

### Set up .gitignore

Create or edit `.gitignore` in the template directory:

```bash
# From template/ directory
cat > .gitignore << 'EOF'
# Optional: exclude personal photos
images/

# Temporary files
*.tmp
.DS_Store
Thumbs.db

# OS files
._.DS_Store

# Editor files
.vscode/
.idea/
EOF
```

**Privacy decision:** Do you want to commit your clothing photos to git?
- **Yes** - Remove `images/` from .gitignore (useful if syncing across devices)
- **No** - Keep `images/` in .gitignore (more private, but photos won't sync)

### Make initial commit

```bash
git add .
git commit -m "Initialize StyleBot wardrobe system"
```

## Step 5: Start Claude Code

### Using VS Code Extension

1. **Open the template folder in VS Code**
   ```bash
   code .
   ```

2. **Open Claude Code panel**
   - Click Claude icon in sidebar, OR
   - Press `Cmd/Ctrl + Shift + P` → "Claude Code: Focus on Chat"

3. **Authenticate** (first time only)
   - You'll be prompted to sign in with your Claude account
   - Follow the authentication flow

4. **Verify you're in the right directory**
   - Claude should show `template/` as working directory

### Using CLI

1. **Navigate to template directory**
   ```bash
   cd my-wardrobe/template
   ```

2. **Start Claude Code**
   ```bash
   claude-code
   ```

3. **Authenticate** (first time only)
   - Follow prompts to authenticate with Claude account

## Step 6: Activate StyleBot Agent

Once Claude Code is running:

1. **Type in chat:**
   ```
   @style-expert
   ```

2. **StyleBot will greet you and show the help menu**
   - You should see the StyleBot persona (icon 👔)
   - List of available commands with `*` prefix

3. **Verify setup by running:**
   ```
   *show-wardrobe
   ```
   - Should show the 2 example items from the templates
   - If you see them, setup is successful!

## Step 7: Add Your First Item

Let's replace the example items with your actual wardrobe:

1. **Prepare an image**
   - Save a clothing image to `images/wardrobe/`
   - Example: `images/wardrobe/MyBrand_Blue_Shirt.png`

2. **Add the item:**
   ```
   *add-item
   ```

3. **Follow StyleBot's prompts:**
   - Provide the image path
   - Claude will analyze the image using vision
   - Review and confirm the auto-generated metadata
   - Item is added to both index and items files

4. **Repeat for a few more items**
   - Start with 5-10 items to get a feel for the system
   - You can bulk-import later with `*bulk-import`

## Step 8: Clean Up Example Data (Optional)

Once you've added your own items, remove the template examples:

1. **Open the data files:**
   - `data/wardrobe/wardrobe_index.json`
   - `data/wardrobe/wardrobe_items.json`

2. **Remove the example items:**
   - Delete `item_20251004_001` and `item_20251004_002`
   - Or use `*remove-item` command

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Added initial wardrobe items"
   ```

## Verification Checklist

Confirm everything is working:

- [ ] Claude Code opens in the `template/` directory
- [ ] `@style-expert` activates StyleBot with greeting
- [ ] `*show-wardrobe` displays items
- [ ] `*add-item` successfully adds a new item
- [ ] Data files are being updated (`data/wardrobe/*.json`)
- [ ] Git is tracking changes (`git status` shows modifications)

## Troubleshooting

### "Authentication failed" or "Invalid API key"

**Problem:** Claude Code can't connect to Claude API

**Solutions:**
1. Verify you have an active Claude Pro or Team subscription
2. Sign out and sign in again in Claude Code
3. Check [status.anthropic.com](https://status.anthropic.com) for service issues
4. Clear Claude Code cache and re-authenticate

### "@style-expert doesn't activate StyleBot"

**Problem:** Agent not found or not loading

**Solutions:**
1. Verify you're in the `template/` directory (not parent directory)
2. Check that `.claude/agents/style-expert-agent.md` exists
3. Try reloading Claude Code window
4. Check Claude Code version is up to date

### "Cannot find wardrobe data files"

**Problem:** StyleBot can't locate `wardrobe_index.json` or `wardrobe_items.json`

**Solutions:**
1. Verify files exist: `ls data/wardrobe/`
2. Check you copied templates correctly (Step 2)
3. Ensure you're in `template/` directory, not subdirectory
4. File paths should be: `data/wardrobe/wardrobe_index.json`

### "Image analysis failed" when adding items

**Problem:** Claude can't process the image file

**Solutions:**
1. Verify image format is PNG, JPG, or JPEG
2. Check image isn't corrupted (can you open it?)
3. Try using a smaller file size (< 5MB works best)
4. Ensure image path is correct and file exists
5. Try using absolute path instead of relative

### "Git commit failed" or merge conflicts

**Problem:** Git is having issues tracking changes

**Solutions:**
1. Check git status: `git status`
2. If conflicts, resolve them manually or:
   ```bash
   git reset --hard HEAD  # WARNING: loses uncommitted changes
   ```
3. Ensure you have git configured:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

### JSON syntax errors

**Problem:** Wardrobe data files have invalid JSON

**Solutions:**
1. Use a JSON validator: [jsonlint.com](https://jsonlint.com)
2. Common issues:
   - Missing commas between items
   - Extra comma after last item in array
   - Mismatched brackets `[]` or braces `{}`
3. Restore from template:
   ```bash
   cp templates/wardrobe/wardrobe_items.template.json data/wardrobe/wardrobe_items.json
   ```

## Next Steps

Now that setup is complete:

1. **Add more wardrobe items** - Use `*bulk-import` for efficiency
2. **Get your first recommendation** - Try `*recommend-outfit`
3. **Read USAGE.md** for detailed command documentation
4. **Start the learning loop** - Wear outfits, rate them, improve recommendations

## Getting Help

- **Documentation:** Read [USAGE.md](USAGE.md) for command examples
- **Architecture:** See [data/wardrobe/README.md](data/wardrobe/README.md) for index structure
- **Issues:** Open an issue on the GitHub repository
- **Claude Code Docs:** [docs.claude.com/claude-code](https://docs.claude.com/claude-code)

---

**Setup complete! Time to build your digital wardrobe.** 🎉

Run `*help` in StyleBot to see all available commands.
