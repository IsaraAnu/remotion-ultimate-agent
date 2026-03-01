# AI Learning Memory
*Core Remotion Workflow & Optimization Rules (Max 20)*

### Architecture & Timing
- **Sequence Architecture:** Break videos into `Sequence` blocks and calculate precise frames using `seconds * fps`.
- **Pacing & Transitions:** Change scenes every 1-3 seconds to maintain engagement, overlapping scenes by 15-30 frames for seamless transitions.
- **Narrative Flow:** Ensure every scene has a distinct visual purpose that builds the story (e.g., Spark → Structure → Reality → Future).

### Animation & Motion
- **Interpolation Safety:** Always apply `extrapolateLeft: 'clamp'` and `extrapolateRight: 'clamp'` to all `interpolate()` calls to prevent boundary errors.
- **Premium Spring:** Use `{ damping: 30, stiffness: 100 }` for high-damping, non-bouncy, professional deceleration.
- **Fluid Easing:** Utilize custom curves like `Easing.inOut(Easing.quad/sin/circle)` for Apple-style smooth motion.
- **Compound Animations:** Combine `interpolate()` calls for position, opacity, and blur within single frame calculations.
- **Text Reveals:** Calculate individual delays (`index * frameOffset`) for cinematic letter-by-letter animations.

### Performance Optimization
- **DOM Constraints:** Keep DOM elements strictly under 150 per frame to ensure stable 60fps rendering and prevent timeouts.
- **GPU Acceleration:** Exclusively use CSS transforms (`translate`, `scale`, `rotate`) instead of position layout changes.
- **Pre-calculation:** Use `React.useMemo` to define static arrays (grids, particles, text segments) outside the render loop.
- **Complexity Limits:** Remove heavy operations like `backdrop-filter` and simplify gradients if the renderer crashes.
- **Test Strategy:** Develop and validate animations at 10-15s intervals before scaling up to the full 60s render.

### Typography & Visuals
- **Safe Zones:** Constrain text within 9:16 boundaries using 8-15% margins, `maxWidth`, and `transform: translateX(-50%)` for perfect centering.
- **Bold Impact:** Maximize vertical presence using ultra-bold typography (weights 800-900) at 60-84px sizes.
- **Depth & Glow:** Add 15-50px colored text shadows for depth and a premium glow effect without heavy SVG filters.
- **3D Depth:** Apply `perspective(800-1200px)` with `rotateX/Y` to create dynamic spatial elements.
- **Visual Continuity:** Maintain a consistent color palette (e.g., cyan-blue 100, 200, 255) across all scene transitions.