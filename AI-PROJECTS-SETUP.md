# AI Projects Page - Setup Guide

## What Was Created

1. **AI Projects Page**: `https://phoenixtbird.com/ai-projects.html`
   - Custom-designed page matching your portfolio
   - Automatically pulls blog posts from WordPress
   - Responsive grid layout
   - Hover effects and smooth transitions

2. **Updated Navigation**: Added "AI Projects" link to main menu

## How to Add AI Projects

### Step 1: Create AI Projects Category in WordPress

1. Log into WordPress: `https://phoenixtbird.com/teaching/wp-admin/`
2. Go to **Posts → Categories**
3. Create a new category:
   - **Name**: AI Projects
   - **Slug**: ai-projects
   - Click **Add New Category**
4. **Note the Category ID**:
   - After creating, hover over the category name
   - Look at the URL in your browser status bar
   - You'll see something like: `...category.php?tag_ID=5`
   - The number (5) is your category ID

### Step 2: Update the Page with Category ID

The file `ai-projects.html` has this line (around line 150):
```javascript
const response = await fetch('https://phoenixtbird.com/teaching/wp-json/wp/v2/posts?categories=AI-PROJECTS-CATEGORY-ID&per_page=12&_embed');
```

**Replace `AI-PROJECTS-CATEGORY-ID` with your actual category ID.**

For example, if your category ID is 5:
```javascript
const response = await fetch('https://phoenixtbird.com/teaching/wp-json/wp/v2/posts?categories=5&per_page=12&_embed');
```

### Step 3: Write Your First AI Project Post

1. Go to **Posts → Add New** in WordPress
2. Write your AI project post:
   - **Title**: Project name (e.g., "AI-Powered Home Inspection Assistant")
   - **Content**: Full project description, code snippets, images, etc.
   - **Category**: Select "AI Projects" checkbox
   - **Featured Image**: Add a project screenshot/image (optional but recommended)
3. Click **Publish**

### Step 4: Test It!

1. Visit: `https://phoenixtbird.com/ai-projects.html`
2. Your project should appear in the grid
3. Click on it to read the full post

## Tips for Great AI Project Posts

### Recommended Structure:

```markdown
## Overview
Brief description of what the project does

## Problem
What problem does it solve?

## Solution
How did you solve it?

## Technologies Used
- Python
- OpenAI API
- etc.

## Results
What did you achieve?

## Code Examples
[Include code snippets]

## Future Improvements
What's next?
```

### Adding Images:
- Click "Add Media" in WordPress editor
- Upload screenshots, diagrams, results
- Featured image shows on the projects grid

### Adding Code:
- Use the "Code" block in WordPress
- Or use triple backticks for syntax highlighting

## Customization Options

### Change Number of Projects Displayed:
In `ai-projects.html`, change `per_page=12` to show more/fewer:
```javascript
...?categories=5&per_page=20&_embed
```

### Change Sort Order:
Add `&orderby=modified` to show recently updated first:
```javascript
...?categories=5&per_page=12&orderby=modified&_embed
```

### Filter by Tag:
You can also filter by tags:
```javascript
...?tags=TAG_ID&per_page=12&_embed
```

## Troubleshooting

### "No AI projects yet" message?
- Make sure you assigned the post to the AI Projects category
- Check that the category ID in the code matches
- Post must be published (not draft)

### Images not showing?
- Upload a Featured Image in WordPress
- The image will automatically display on the grid

### Projects not linking?
- Make sure the post is published
- Check browser console for errors (F12)

## Next Steps

1. Find your AI Projects category ID
2. Update ai-projects.html with the correct ID
3. Upload the updated file
4. Write your first AI project post!
5. Share your projects page!

---

Your AI projects page is live at: **https://phoenixtbird.com/ai-projects.html**
