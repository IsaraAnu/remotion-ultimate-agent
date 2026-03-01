# AI Learning Memory 
*This file stores high-value insights and error fixes.* 
 
### Learned Insights: 
- Initialized memory for Remotion workflow. 

- When creating a multi-part animation sequence in Remotion, it's crucial to calculate frame numbers precisely based on the video's FPS. Using `sequenceOffset` and the formula `startFrame + (timeInSeconds * fps)` ensures accurate timing for each visual element across different segments of the composition.
- The scan line interpolation was calculated using interpolate(frame, [0, fps * duration], [start_pos, end_pos]). The 'ACCESS GRANTED' text used a spring animation that started at frame 150, offset from the main timeline.
- When interpolating position changes for multiple objects, it's essential to pre-calculate static intermediate values (like the exploded positions) outside the loop to avoid runtime errors caused by passing incorrect array lengths to the interpolate function.
- Achieving Apple-style smooth easing in Remotion relies heavily on tuning the 'spring' animation config. A combination of lower 'stiffness' (e.g., 100) and higher 'damping' (e.g., 30) values creates the characteristic gentle, non-bouncy motion.
- The seamless transition between Act 2 and Act 3 was achieved by having the visual elements of Act 2 (the hyperspeed lines) gradually fade out while the static stars for Act 3 were already present, creating a continuous sense of motion that slowed down into stillness.
- MANAGING COMPLEX 60-SECOND TRANSITIONS IN REMOTION:

1. SEQUENCE MANAGEMENT: For multi-phase videos (60s+), break content into distinct Sequence blocks with precise frame calculations (frame = seconds × fps). Each phase should have clear entry/exit points to prevent animation conflicts.

2. INTERPOLATION STRATEGY: Use interpolate() with extrapolateLeft/Right: 'clamp' for all time-based animations to prevent values from exceeding bounds at sequence boundaries. For premium motion, implement custom Easing.bezier(0.25, 0.1, 0.25, 1) curves instead of default easings.

3. PERFORMANCE OPTIMIZATION: 
   - Pre-calculate static arrays (grid lines, particles) outside render loops
   - Limit DOM elements per frame (< 200 recommended for 60fps)
   - Use CSS transforms over position changes for GPU acceleration
   - Implement opacity fade-outs before heavy element creation

4. TRANSITION TECHNIQUES:
   - Overlap sequences by 15-30 frames for seamless phase changes
   - Use liquidProgress variables to morph between visual states
   - Combine multiple interpolate() calls for compound animations (position + opacity + blur)

5. SPRING ANIMATION TUNING: For high-damping premium feel, use spring config: { damping: 30, stiffness: 100 }. Lower stiffness prevents bounce, higher damping creates smooth deceleration.

6. RENDER CONSIDERATIONS: 60-second videos at 60fps (3600 frames) require significant render time. Consider testing with shorter durations (10-15s) during development, then scale up for final render. Monitor frame complexity to avoid timeout errors.

7. TEXT REVEAL PATTERNS: For letter-by-letter reveals, calculate individual delays (index × frameOffset) and apply combined transform (translateY) + opacity + blur filters for cinematic effect.
- MANAGING COMPLEX 60-SECOND TRANSITIONS IN REMOTION: Render timeouts are common for long, complex videos (60s, 60fps = 3600 frames). The system may struggle with performance due to the high number of calculations per frame, especially with complex SVG filters, numerous interpolate() calls, and overlapping Sequences. To mitigate, consider: 1. Simplifying complex effects like SVG filters or expensive CSS properties (e.g., multiple blurs) for initial renders. 2. Breaking the video into smaller compositions for development. 3. Optimizing code for performance before the final render. 4. Running the render command in a more powerful environment if possible.
- ASSET LOADING ISSUE: When list_local_assets shows files in 'remotion-studio/assets' but staticFile() looks in 'public/', there may be a path mismatch. Workaround: Use inline SVG components for logos when external assets fail to load (404 errors).

RENDER TIMEOUT OPTIMIZATION: For 60fps videos, reduce complexity to avoid MCP timeout errors:
- Limit 3D layer stacks to 5 layers instead of 10+
- Use hardcoded frame values instead of fps calculations
- Simplify interpolate calls and pre-calculate durations
- For 20s@60fps (1200 frames), consider testing at 10s@60fps (600 frames) first
- Complex transforms with multiple layers significantly increase render time