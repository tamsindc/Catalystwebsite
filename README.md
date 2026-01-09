# fshpind.ai - Interactive Homepage

An interactive, fun homepage for fshpind - an app that helps users discover and install AI workflows and use cases.

## Features

### 🎨 Interactive Design
- Animated floating particles background
- 3D tilt effects on feature cards
- Smooth scroll animations
- Interactive button effects with ripple animations
- Parallax scrolling effects

### 🎯 Sections
1. **Hero Section** - Eye-catching introduction with animated logo and floating squares
2. **Features** - Showcase of key product features with interactive cards
3. **Workflows** - Display of popular AI workflows with install buttons
4. **CTA Section** - Download buttons for different platforms
5. **Footer** - Navigation and social links

### 🎮 Easter Eggs
- Konami Code support (↑↑↓↓←→←→BA)
- Animated button interactions
- Hidden console messages

## Setup

1. **Add Your Logo**
   - Place your `fishpond-logo.png` in the `assets/images/` directory
   - The logo is referenced in multiple places (navbar, hero, footer)

2. **Open the Website**
   - Simply open `index.html` in a modern web browser
   - Or serve with a local server for best experience

3. **Customize**
   - Edit colors in `styles.css` (CSS variables in `:root`)
   - Modify content in `index.html`
   - Adjust animations in `script.js`

## Color Scheme

Based on the fshpind.ai branding:
- Navy Blue: `#1a3a6b`
- Yellow: `#FFB300`
- Orange: `#E85D3F`
- Cyan: `#00BCD4`

## Browser Support

Works best in modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Files

- `index.html` - Main HTML structure
- `styles.css` - All styling and animations
- `script.js` - Interactive JavaScript features
- `assets/images/` - Image assets directory

## Customization Tips

### Change Colors
Edit the CSS variables in `styles.css`:
```css
:root {
    --navy: #1a3a6b;
    --yellow: #FFB300;
    --orange: #E85D3F;
    --cyan: #00BCD4;
}
```

### Add More Workflows
Add workflow cards in the workflows section of `index.html`:
```html
<div class="workflow-card">
    <div class="workflow-header">
        <span class="workflow-category">Category</span>
        <span class="workflow-rating">⭐ 5.0</span>
    </div>
    <h3>Workflow Name</h3>
    <p>Description</p>
    <button class="workflow-btn">Install Workflow</button>
</div>
```

### Modify Animations
Adjust animation speeds in `styles.css` by changing animation duration values.

## Performance

- Debounced scroll events for better performance
- Optimized animations using CSS transforms
- Lazy-loaded animations using Intersection Observer

## Future Enhancements

- [ ] Add actual download functionality
- [ ] Integrate with backend API for real workflows
- [ ] Add search functionality
- [ ] User authentication
- [ ] Workflow rating system

---

Built with ❤️ for fshpind.ai
