# Everyday Essentials - Amazon Affiliate Site

A ready-to-deploy website featuring 96 everyday essential products with automatic Amazon affiliate link deep linking.

## 🚀 Quick Start

### 1. Configure Your Affiliate ID

Edit `config.js` and replace `YOUR-AFFILIATE-ID-20` with your actual Amazon Associates tracking ID:

```javascript
affiliateId: 'your-actual-id-20'
```

You can find your Amazon Associates tracking ID in your [Amazon Associates account](https://affiliate-program.amazon.com/).

### 2. Test Locally

Simply open `index.html` in a web browser to test locally.

### 3. Deploy to the Internet

Choose one of the following deployment options:

## 🌐 Deployment Options

### Option 1: GitHub Pages (Free & Easy)

1. Push this repository to GitHub
2. Go to repository Settings → Pages
3. Select branch (usually `main` or `master`)
4. Click Save
5. Your site will be live at `https://yourusername.github.io/repository-name/`

**Setup:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### Option 2: Netlify (Free with Custom Domain)

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start)

1. Sign up at [Netlify](https://netlify.com)
2. Drag and drop the project folder into Netlify
3. Your site will be live instantly with a custom subdomain
4. Optionally add your own domain

**Or use Netlify CLI:**
```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Option 3: Vercel (Free with Excellent Performance)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

1. Sign up at [Vercel](https://vercel.com)
2. Import your GitHub repository or drag and drop files
3. Click Deploy
4. Your site will be live with automatic HTTPS

**Or use Vercel CLI:**
```bash
npm install -g vercel
vercel --prod
```

### Option 4: Cloudflare Pages (Free with CDN)

1. Sign up at [Cloudflare Pages](https://pages.cloudflare.com/)
2. Connect your GitHub repository
3. Click Deploy
4. Your site will be live with global CDN

### Option 5: AWS S3 + CloudFront

For advanced users wanting full control:

1. Create an S3 bucket
2. Enable static website hosting
3. Upload files
4. Configure CloudFront for HTTPS
5. Point your domain

## 📋 Features

- ✅ **96 Product Links** - Curated everyday essentials across 12 categories
- ✅ **Live Product Search** - Instantly filter products by name or description
- ✅ **Dark Mode** - Toggle between light and dark themes (preference saved locally)
- ✅ **Category Navigation** - Quick jump links to browse products by category
- ✅ **Back to Top Button** - Smooth scroll navigation for better user experience
- ✅ **Automatic Affiliate Deep Linking** - All Amazon links automatically include your affiliate ID
- ✅ **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- ✅ **Smooth Animations** - Modern fade-in and hover effects for enhanced UX
- ✅ **No Backend Required** - Pure HTML/CSS/JavaScript
- ✅ **Easy to Customize** - Simple configuration file
- ✅ **Fast Loading** - Optimized for performance
- ✅ **SEO Friendly** - Proper meta tags, Open Graph, and Twitter Card support

## 🛠️ Customization

### Adding More Products

Edit `index.html` and add new product cards:

```html
<div class="product-card">
    <h4>Product Name</h4>
    <p>Product Description</p>
    <a href="https://www.amazon.com/dp/PRODUCT-ASIN" class="amazon-link" data-product="Product Name">
        View on Amazon
    </a>
</div>
```

### Changing Styles

Edit `styles.css` to modify colors, fonts, and layout:

```css
:root {
    --primary-color: #FF9900;  /* Amazon orange */
    --secondary-color: #146EB4; /* Amazon blue */
}
```

### Analytics Integration

Add Google Analytics by including in `index.html` before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Different Amazon Stores

To use Amazon stores in different countries, update `config.js`:

```javascript
amazonDomain: 'amazon.co.uk',  // For UK
// or 'amazon.de' for Germany
// or 'amazon.ca' for Canada
```

## 📦 Product Categories

The site features 12 comprehensive product categories with 96 total products:

1. **🍳 Kitchen Essentials** - Cookware, appliances, and kitchen tools
2. **🧴 Personal Care** - Grooming, hygiene, and beauty products
3. **🏡 Home Essentials** - Home improvement and organization
4. **📱 Electronics** - Tech gadgets and accessories
5. **🏋️ Fitness & Sports** - Exercise equipment and fitness gear
6. **👶 Baby & Kids** - Children's products and toys
7. **🖊️ Office Supplies** - Stationery and office essentials
8. **🐾 Pet Supplies** - Pet care products and accessories
9. **🚗 Automotive** - Car care and accessories
10. **🌱 Garden & Outdoor** - Gardening tools and outdoor products
11. **💊 Health & Wellness** - Health monitoring and wellness products
12. **✈️ Travel & Luggage** - Travel accessories and organizers

Use the category navigation menu to quickly jump to any category section.

## 📁 File Structure

```
.
├── index.html          # Main HTML page with products
├── styles.css          # CSS styling
├── config.js           # Affiliate configuration
├── affiliate.js        # Automatic link processing
├── enhancements.js     # Live search and dark mode
├── README.md           # This file
├── netlify.toml        # Netlify configuration
└── vercel.json         # Vercel configuration
```

## 🔧 Technical Details

### How Affiliate Link Deep Linking Works

1. The `config.js` file stores your Amazon Associates tracking ID
2. When the page loads, `affiliate.js` finds all Amazon links
3. It automatically appends your tracking ID as a URL parameter (`?tag=your-id-20`)
4. All links open in a new tab for better user experience
5. Optional click tracking for analytics

### Browser Compatibility

- ✅ Chrome, Firefox, Safari, Edge (latest versions)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)
- ✅ No external dependencies required

## 📝 Best Practices

1. **Update Your Affiliate ID** - Don't forget to set your actual ID in `config.js`
2. **Test Links** - Click a few links to ensure they work and include your tag
3. **Add Content** - Customize products based on your niche
4. **Drive Traffic** - Share on social media, blogs, email lists
5. **Monitor Performance** - Use Amazon Associates dashboard to track earnings
6. **Stay Compliant** - Follow [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/agreement)

## 🚨 Important Compliance Note

This site includes the required affiliate disclosure. According to FTC guidelines and Amazon Associates Operating Agreement, you must:

- ✅ Clearly disclose affiliate relationships
- ✅ Not modify or obfuscate Amazon links
- ✅ Follow Amazon's branding guidelines
- ✅ Update links if products become unavailable

## 💡 Tips for Success

1. **Choose Your Niche** - Focus on products you know and trust
2. **Write Reviews** - Add detailed product reviews to increase trust
3. **Update Regularly** - Keep products current and remove discontinued items
4. **SEO Optimization** - Add meta descriptions and proper headings
5. **Build Trust** - Only recommend products you would use yourself

## 📊 Tracking Your Success

Check your Amazon Associates dashboard regularly:
- View clicks and conversions
- See earnings per product
- Analyze traffic sources
- Optimize based on performance

## 🆘 Support

For Amazon Associates support:
- [Amazon Associates Help](https://affiliate-program.amazon.com/help)
- [Amazon Associates Blog](https://affiliate-program.amazon.com/blog)

For website issues:
- Check browser console for JavaScript errors
- Verify affiliate ID is set correctly in `config.js`
- Ensure all files are uploaded to your hosting

## 📄 License

This project is free to use for personal and commercial purposes. Feel free to modify and adapt it for your needs.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

---

**Ready to start earning? Configure your affiliate ID and deploy now!** 🚀
