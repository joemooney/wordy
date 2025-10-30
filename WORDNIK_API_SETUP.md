# Wordnik API Setup for Letter Grid Game

The Letter Grid game's Review Panel uses the Wordnik API to show word definitions and examples. This is an optional feature that requires a free API key.

## Why You Need This

Without the API key configured, the Review Panel will show:
- "No definitions found" for all words
- An error message about missing API key

With the API key, you'll see:
- Up to 3 definitions for each word
- Up to 3 example sentences
- Part of speech information

## Quick Setup (5 minutes)

### Step 1: Get a Free API Key

1. Visit https://developer.wordnik.com/
2. Click "Sign Up" (or "Log In" if you have an account)
3. Fill out the simple form
4. Verify your email
5. Once logged in, go to "API Key" section
6. Copy your API key (looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p`)

### Step 2: Add Your API Key to the Code

**Option A: Edit in a Text Editor**
1. Open `templates/letter_grid.html` in any text editor
2. Find line **1290** (search for `YOUR_API_KEY_HERE`)
3. Replace `'YOUR_API_KEY_HERE'` with your actual key
4. Example:
   ```javascript
   // Before:
   const WORDNIK_API_KEY = 'YOUR_API_KEY_HERE';

   // After:
   const WORDNIK_API_KEY = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p';
   ```
5. Save the file
6. Refresh your browser

**Option B: Use Command Line**
```bash
# From the wordy directory
# Replace YOUR_ACTUAL_KEY with your real API key
sed -i "s/YOUR_API_KEY_HERE/YOUR_ACTUAL_KEY/" templates/letter_grid.html
```

### Step 3: Test It

1. Open the Letter Grid game
2. Find or submit a word
3. Click "📋 Review Words" button
4. Click on any word
5. You should now see definitions and examples!

## Troubleshooting

### Still Seeing "No definitions found"

**Check 1: API Key Format**
- Make sure the key is in quotes: `'your-key-here'`
- No spaces before or after the key
- No extra characters

**Check 2: Browser Console**
- Press F12 to open browser developer tools
- Look at the Console tab
- Check for error messages about the API

**Check 3: API Key Status**
- Log into https://developer.wordnik.com/
- Check if your API key is active
- Check if you've hit any rate limits (unlikely with normal use)

### Error: "Invalid API key"

Your API key might be:
- Copied incorrectly (extra spaces/characters)
- Expired or deactivated
- Try generating a new key from Wordnik

### Error: "Failed to fetch"

This might be:
- CORS or network issue
- Check your internet connection
- Try refreshing the page

## API Usage Limits

Wordnik's free tier includes:
- **15,000 requests per hour**
- **Unlimited requests per day**

This is more than enough for personal use. Each word lookup uses 2 requests (definitions + examples), so you can look up ~7,500 words per hour.

## Privacy & Security

**Is my API key secure?**
- The API key is stored in the HTML file (client-side only)
- It's visible in the browser's source code
- This is fine for a free API key with limited scope
- Don't share your HTML file publicly if you want to keep the key private
- You can always regenerate a new key at Wordnik

**What data is sent?**
- Only the word you're looking up
- No personal information
- No game data
- Just a simple API request for word definitions

## Alternative: Use Without API

The Review Panel still works without the Wordnik API! You can:
- Review all pending delete words
- Review all disputed words
- Review all valid words
- Permanently delete or approve words
- See the word count and status

You just won't see definitions and examples from Wordnik.

## Need Help?

- **Wordnik API Docs**: https://developer.wordnik.com/docs
- **Wordnik Support**: Contact via their website
- **Game Issues**: Check REQUIREMENTS.md and PROMPT_HISTORY.md

---

*Last Updated: 2025-10-29*
