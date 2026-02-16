# Quick Setup Guide

## Step 1: Configure Your Amazon Affiliate ID

1. Open `config.js` in a text editor
2. Replace `YOUR-AFFILIATE-ID-20` with your actual Amazon Associates tracking ID
   - Example: `mystore-20` or `johndoe-21`
3. Save the file

```javascript
affiliateId: 'mystore-20',  // Replace with your ID
```

## Step 2: Test Locally

1. Open `index.html` in your web browser
2. Click on any product link
3. Verify the URL includes your affiliate ID: `?tag=your-id-20`

## Step 3: Deploy to the Internet

### Option A: GitHub Pages (Recommended - Free)

1. Create a GitHub repository
2. Push these files to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/USERNAME/REPO.git
   git push -u origin main
   ```
3. Go to repository Settings → Pages
4. Select the `main` branch as the source
5. Your site will be live at: `https://USERNAME.github.io/REPO/`

### Option B: Netlify (Free with Custom Domain)

1. Sign up at [netlify.com](https://netlify.com)
2. Drag and drop your project folder
3. Done! Your site is live with HTTPS

### Option C: Vercel (Free with Great Performance)

1. Sign up at [vercel.com](https://vercel.com)
2. Import your GitHub repository or upload files
3. Click Deploy
4. Your site is live!

## Step 4: Drive Traffic

- Share on social media
- Add to email signature
- Promote on your blog or YouTube channel
- Use SEO optimization

## Features Included

✅ 96 curated everyday essential products  
✅ 12 product categories  
✅ Category navigation with quick jump links  
✅ Back-to-top button for easy navigation  
✅ Smooth scroll and modern animations  
✅ Automatic affiliate link deep linking  
✅ Responsive mobile-friendly design  
✅ Click tracking support  
✅ Warning banner if affiliate ID not set  
✅ Compliance-ready disclosure section  

## Support

- For Amazon Associates: [affiliate-program.amazon.com/help](https://affiliate-program.amazon.com/help)
- Check browser console (F12) for any JavaScript errors
- Ensure config.js is loaded before affiliate.js

## Customization Tips

1. **Add more products**: Edit `index.html` and add product cards
2. **Change colors**: Edit CSS variables in `styles.css`
3. **Add analytics**: Include Google Analytics in `index.html`
4. **Different Amazon region**: Change `amazonDomain` in `config.js`

---

**Ready to earn? Configure your ID and deploy!** 🚀
