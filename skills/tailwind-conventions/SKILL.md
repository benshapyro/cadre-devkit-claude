# Tailwind CSS Conventions Skill

Consistent patterns for Tailwind CSS in React/Next.js applications.

## Class Organization Order

Always organize classes in this order for readability:

```tsx
className={cn(
  // 1. Layout (position, display, flex/grid)
  "relative flex flex-col",
  // 2. Sizing (width, height, padding, margin)
  "w-full max-w-md p-4 mx-auto",
  // 3. Visual (background, border, shadow)
  "bg-white border border-gray-200 rounded-lg shadow-sm",
  // 4. Typography (font, text, color)
  "text-sm font-medium text-gray-900",
  // 5. States (hover, focus, active, disabled)
  "hover:bg-gray-50 focus:ring-2 focus:ring-blue-500",
  // 6. Responsive (sm:, md:, lg:, xl:)
  "md:flex-row md:p-6",
  // 7. Dark mode
  "dark:bg-gray-800 dark:text-white"
)}
```

## Utility Function (cn)

Use `clsx` + `tailwind-merge` for conditional classes:

```tsx
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
<div className={cn(
  "base-classes",
  isActive && "active-classes",
  variant === "primary" && "primary-classes"
)} />
```

## Responsive Design

### Mobile-First Approach
```tsx
// Start with mobile, add breakpoints for larger screens
<div className="
  flex flex-col gap-2      // Mobile: stack vertically
  md:flex-row md:gap-4     // Tablet+: horizontal row
  lg:gap-6                 // Desktop: more spacing
" />
```

### Common Breakpoints
- `sm:` - 640px+ (large phones)
- `md:` - 768px+ (tablets)
- `lg:` - 1024px+ (laptops)
- `xl:` - 1280px+ (desktops)
- `2xl:` - 1536px+ (large screens)

### Responsive Typography
```tsx
<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold" />
<p className="text-sm md:text-base" />
```

## Dark Mode

### Using CSS Variables (Recommended)
```css
/* globals.css */
:root {
  --background: 255 255 255;
  --foreground: 10 10 10;
}

.dark {
  --background: 10 10 10;
  --foreground: 255 255 255;
}
```

```tsx
// tailwind.config.ts
theme: {
  extend: {
    colors: {
      background: 'rgb(var(--background) / <alpha-value>)',
      foreground: 'rgb(var(--foreground) / <alpha-value>)',
    }
  }
}

// Usage - no dark: prefix needed
<div className="bg-background text-foreground" />
```

### Using dark: Prefix
```tsx
<div className="
  bg-white text-gray-900
  dark:bg-gray-900 dark:text-white
" />
```

## Component Patterns

### Button Variants
```tsx
const buttonVariants = {
  base: "inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
  variants: {
    primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-500",
    outline: "border border-gray-300 bg-transparent hover:bg-gray-50 focus:ring-gray-500",
    ghost: "bg-transparent hover:bg-gray-100 focus:ring-gray-500",
    destructive: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
  },
  sizes: {
    sm: "h-8 px-3 text-sm",
    md: "h-10 px-4 text-sm",
    lg: "h-12 px-6 text-base",
  }
};
```

### Card Pattern
```tsx
<div className="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-950">
  <div className="p-6">
    <h3 className="text-lg font-semibold">Title</h3>
    <p className="text-sm text-gray-500 dark:text-gray-400">Description</p>
  </div>
</div>
```

### Input Pattern
```tsx
<input className="
  flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2
  text-sm placeholder:text-gray-400
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
  disabled:cursor-not-allowed disabled:opacity-50
  dark:border-gray-700 dark:bg-gray-900
" />
```

## Spacing Conventions

### Consistent Spacing Scale
- `gap-1` / `p-1` = 4px (tight)
- `gap-2` / `p-2` = 8px (compact)
- `gap-4` / `p-4` = 16px (default)
- `gap-6` / `p-6` = 24px (comfortable)
- `gap-8` / `p-8` = 32px (spacious)

### Container Pattern
```tsx
<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
  {/* Content */}
</div>
```

## Animation

### Transitions
```tsx
// Smooth color/opacity transitions
<button className="transition-colors duration-200" />

// Transform transitions (scale, translate)
<div className="transition-transform duration-200 hover:scale-105" />

// All properties
<div className="transition-all duration-300" />
```

### Built-in Animations
```tsx
<div className="animate-spin" />     // Loading spinner
<div className="animate-pulse" />    // Skeleton loading
<div className="animate-bounce" />   // Attention grabber
<div className="animate-ping" />     // Notification dot
```

## Accessibility

### Focus States
```tsx
// Always visible focus rings
<button className="
  focus:outline-none
  focus:ring-2
  focus:ring-blue-500
  focus:ring-offset-2
" />

// Focus-visible for keyboard only
<button className="
  focus-visible:outline-none
  focus-visible:ring-2
  focus-visible:ring-blue-500
" />
```

### Screen Reader
```tsx
<span className="sr-only">Loading...</span>  // Hidden visually, announced
<div aria-hidden="true" className="..." />   // Decorative, ignored
```

## Anti-Patterns

- Don't use `@apply` excessively - defeats Tailwind's purpose
- Don't create overly specific custom classes
- Don't fight the spacing scale - use what's provided
- Don't inline complex conditional logic - extract to variables
- Don't forget dark mode when adding colors
- Don't use arbitrary values `[123px]` when scale values exist
