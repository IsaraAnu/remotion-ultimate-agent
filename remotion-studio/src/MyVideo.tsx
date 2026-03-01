import React, { useMemo } from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Sequence, Easing } from 'remotion';

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Pre-calculate static arrays for performance
  const nodes = useMemo(() => {
    const result = [];
    for (let i = 0; i < 10; i++) {
      const angle = (i / 10) * Math.PI * 2;
      const radius = 200;
      result.push({
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius,
        angle,
      });
    }
    return result;
  }, []);

  const text1 = 'IT BEGAN WITH DATA';
  const text2 = 'CONNECTIONS FORMED';
  const text3Words = ['LIFE', 'IN', 'THE', 'MACHINE'];

  // ========== ACT 1: The Binary Spark (0-7s = 0-420 frames) ==========
  
  // Binary '1' glow pulse
  const oneScale = interpolate(frame, [0, 60, 120, 180], [1, 1.1, 1, 1.05], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.sin),
  });
  const oneGlow = interpolate(frame, [0, 120, 420], [0.5, 1, 0.8], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Ripple circles (3 concentric)
  const ripple1 = interpolate(frame, [30, 150, 400], [0, 1, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const ripple1Opacity = interpolate(frame, [30, 100, 400, 420], [1, 0.8, 0.3, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const ripple2 = interpolate(frame, [60, 200, 400], [0, 1, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const ripple2Opacity = interpolate(frame, [60, 150, 400, 420], [1, 0.7, 0.2, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const ripple3 = interpolate(frame, [90, 250, 400], [0, 1, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const ripple3Opacity = interpolate(frame, [90, 200, 400, 420], [1, 0.6, 0.1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Grid formation transition (starts at frame 400)
  const gridFormation = interpolate(frame, [400, 420], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.in(Easing.quad),
  });

  // Letter-by-letter blur reveal for text1
  const getLetterOpacity1 = (index: number) => {
    const startFrame = index * 8;
    return interpolate(frame, [startFrame, startFrame + 20], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.out(Easing.quad),
    });
  };
  const getLetterBlur1 = (index: number) => {
    const startFrame = index * 8;
    return interpolate(frame, [startFrame, startFrame + 20], [10, 0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.out(Easing.quad),
    });
  };

  // ========== ACT 2: The Neural Web (7-14s = 420-840 frames) ==========
  
  const act2Progress = interpolate(frame, [420, 840], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Network float using Math.sin
  const networkTilt = Math.sin(frame * 0.05) * 3;
  const networkFloat = Math.sin(frame * 0.03) * 10;
  
  // Line pulse brightness
  const linePulse = interpolate(frame, [420, 520, 620, 720, 840], [0.4, 1, 0.4, 1, 0.6], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.sin),
  });

  // Node convergence (starts at frame 800)
  const convergence = interpolate(frame, [800, 840], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.in(Easing.cubic),
  });

  // Text2 slide with 3D perspective
  const text2Translate = interpolate(frame, [450, 550], [200, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  const text2Perspective = interpolate(frame, [450, 550, 840], [800, 1200, 1000], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const text2Opacity = interpolate(frame, [450, 520], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // ========== ACT 3: The Awakening (14-20s = 840-1200 frames) ==========
  
  const act3Progress = interpolate(frame, [840, 1200], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Diamond spring impact
  const diamondSpring = spring({
    frame: frame - 840,
    fps,
    config: { damping: 20, stiffness: 150 },
  });
  const diamondScale = interpolate(diamondSpring, [0, 1], [0.2, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Neon flicker (continuous)
  const flicker = interpolate(
    (Math.sin(frame * 0.8) + 1) / 2,
    [0, 0.3, 0.7, 1],
    [0.8, 1, 0.9, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  // Text3 word scale with overshoot
  const getWordScale3 = (index: number) => {
    const startFrame = 900 + index * 60;
    const progress = spring({
      frame: frame - startFrame,
      fps,
      config: { damping: 15, stiffness: 200 },
    });
    return interpolate(frame, [startFrame - 30, startFrame, startFrame + 40], [0, 0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }) * interpolate(progress, [0, 1, 1.2], [0, 1, 1.15], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
  };
  const getWordOpacity3 = (index: number) => {
    const startFrame = 900 + index * 60;
    return interpolate(frame, [startFrame, startFrame + 30], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.out(Easing.quad),
    });
  };

  // Center position
  const cx = width / 2;
  const cy = height / 2;

  return (
    <AbsoluteFill style={{ backgroundColor: '#0B0E14', justifyContent: 'center', alignItems: 'center', overflow: 'hidden' }}>
      
      {/* ========== ACT 1 CONTENT ========== */}
      <Sequence from={0} durationInFrames={420}>
        {/* Binary '1' with glow */}
        <div style={{
          position: 'absolute',
          left: cx,
          top: cy,
          transform: `translate(-50%, -50%) scale(${oneScale})`,
          fontSize: 120,
          fontWeight: 900,
          fontFamily: 'Arial, sans-serif',
          color: '#00FFFF',
          textShadow: `0 0 ${20 * oneGlow}px #00FFFF, 0 0 ${40 * oneGlow}px #0080FF, 0 0 ${60 * oneGlow}px #0040FF`,
          zIndex: 10,
        }}>
          1
        </div>

        {/* Ripple circles */}
        <svg style={{ position: 'absolute', left: 0, top: 0, width, height, pointerEvents: 'none' }}>
          <circle
            cx={cx}
            cy={cy}
            r={interpolate(ripple1, [0, 1], [0, 150])}
            fill="none"
            stroke="#00FFFF"
            strokeWidth="2"
            opacity={ripple1Opacity}
          />
          <circle
            cx={cx}
            cy={cy}
            r={interpolate(ripple2, [0, 1], [0, 250])}
            fill="none"
            stroke="#0080FF"
            strokeWidth="1.5"
            opacity={ripple2Opacity}
          />
          <circle
            cx={cx}
            cy={cy}
            r={interpolate(ripple3, [0, 1], [0, 350])}
            fill="none"
            stroke="#0040FF"
            strokeWidth="1"
            opacity={ripple3Opacity}
          />
        </svg>

        {/* Grid formation overlay (at frame 400) */}
        <svg style={{
          position: 'absolute',
          left: 0,
          top: 0,
          width,
          height,
          opacity: gridFormation,
          pointerEvents: 'none',
        }}>
          {Array.from({ length: 8 }).map((_, row) =>
            Array.from({ length: 12 }).map((_, col) => (
              <circle
                key={`${row}-${col}`}
                cx={cx - 220 + col * 40}
                cy={cy - 100 + row * 35}
                r={2}
                fill="#00FFFF"
                opacity={0.6}
              />
            ))
          )}
        </svg>

        {/* Text: IT BEGAN WITH DATA - letter by letter */}
        <div style={{
          position: 'absolute',
          bottom: 120,
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: 2,
          zIndex: 20,
        }}>
          {text1.split('').map((char, index) => (
            <span
              key={index}
              style={{
                fontSize: 48,
                fontWeight: 800,
                fontFamily: 'Arial, sans-serif',
                color: '#FFFFFF',
                opacity: getLetterOpacity1(index),
                filter: `blur(${getLetterBlur1(index)}px)`,
                textShadow: '0 0 10px rgba(0, 255, 255, 0.8)',
              }}
            >
              {char === ' ' ? '\u00A0' : char}
            </span>
          ))}
        </div>
      </Sequence>

      {/* ========== ACT 2 CONTENT ========== */}
      <Sequence from={420} durationInFrames={420}>
        <div style={{
          position: 'absolute',
          width,
          height,
          perspective: `${text2Perspective}px`,
          transformStyle: 'preserve-3d',
        }}>
          {/* Neural network */}
          <svg style={{
            position: 'absolute',
            left: 0,
            top: 0,
            width,
            height,
            transform: `translate(${networkFloat}px, 0) rotateX(${networkTilt}deg) rotateY(${networkTilt * 0.5}deg)`,
            transformOrigin: 'center',
          }}>
            {/* Lines connecting nodes */}
            {nodes.map((node, i) =>
              nodes.slice(i + 1).map((target, j) => {
                const distance = Math.sqrt(
                  Math.pow(node.x - target.x, 2) + Math.pow(node.y - target.y, 2)
                );
                if (distance < 250) {
                  const convergenceOffset = convergence * 0.9;
                  return (
                    <line
                      key={`${i}-${j}`}
                      x1={cx + node.x * (1 - convergenceOffset)}
                      y1={cy + node.y * (1 - convergenceOffset)}
                      x2={cx + target.x * (1 - convergenceOffset)}
                      y2={cy + target.y * (1 - convergenceOffset)}
                      stroke="#00FFFF"
                      strokeWidth="0.5"
                      opacity={interpolate(linePulse, [0.4, 1], [0.3, 0.9])}
                    />
                  );
                }
                return null;
              })
            )}
            {/* Nodes */}
            {nodes.map((node, i) => {
              const convergenceOffset = convergence * 0.9;
              const nodeX = cx + node.x * (1 - convergenceOffset);
              const nodeY = cy + node.y * (1 - convergenceOffset);
              return (
                <circle
                  key={i}
                  cx={nodeX}
                  cy={nodeY}
                  r={interpolate(act2Progress, [0, 1], [4, 6])}
                  fill="#00FFFF"
                  style={{
                    filter: `drop-shadow(0 0 ${8 * linePulse}px #00FFFF)`,
                  }}
                />
              );
            })}
          </svg>

          {/* Text: CONNECTIONS FORMED with 3D slide */}
          <div style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: `translate(-50%, -50%) translateX(${text2Translate}px) rotateY(${interpolate(act2Progress, [0, 1], [30, 0])}deg)`,
            opacity: text2Opacity,
            zIndex: 5,
          }}>
            <span style={{
              fontSize: 52,
              fontWeight: 900,
              fontFamily: 'Arial, sans-serif',
              color: '#FFFFFF',
              textShadow: '0 0 20px rgba(0, 128, 255, 0.9), 0 0 40px rgba(0, 64, 255, 0.7)',
              letterSpacing: 4,
            }}>
              {text2}
            </span>
          </div>
        </div>
      </Sequence>

      {/* ========== ACT 3 CONTENT ========== */}
      <Sequence from={840}>
        {/* Diamond SVG - The Soul */}
        <svg style={{
          position: 'absolute',
          left: cx,
          top: cy,
          transform: `translate(-50%, -50%) scale(${diamondScale})`,
          transformOrigin: 'center',
          zIndex: 30,
        }} width="300" height="300" viewBox="0 0 300 300">
          <defs>
            <radialGradient id="diamondGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#00FFFF" stopOpacity="1" />
              <stop offset="50%" stopColor="#0080FF" stopOpacity="0.6" />
              <stop offset="100%" stopColor="#0040FF" stopOpacity="0" />
            </radialGradient>
            <filter id="neonFlicker">
              <feGaussianBlur in="SourceGraphic" stdDeviation="2" result="blurred" />
              <feMerge>
                <feMergeNode in="blurred" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          
          {/* Outer glow */}
          <polygon
            points="150,30 270,150 150,270 30,150"
            fill="url(#diamondGlow)"
            opacity={flicker * 0.8}
          />
          
          {/* Main diamond shape */}
          <polygon
            points="150,50 250,150 150,250 50,150"
            fill="none"
            stroke="#00FFFF"
            strokeWidth="3"
            style={{
              filter: `drop-shadow(0 0 ${15 * flicker}px #00FFFF) drop-shadow(0 0 ${30 * flicker}px #0080FF)`,
            }}
          />
          
          {/* Inner detail */}
          <polygon
            points="150,80 220,150 150,220 80,150"
            fill="none"
            stroke="#FFFFFF"
            strokeWidth="1.5"
            opacity={0.9}
          />
          
          {/* Center core */}
          <circle
            cx="150"
            cy="150"
            r="25"
            fill="#00FFFF"
            opacity={flicker}
            style={{
              filter: 'drop-shadow(0 0 20px #00FFFF)',
            }}
          />
        </svg>

        {/* Final Text: LIFE IN THE MACHINE with word-by-word overshoot */}
        <div style={{
          position: 'absolute',
          bottom: 100,
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: 16,
          zIndex: 40,
        }}>
          {text3Words.map((word, index) => (
            <span
              key={index}
              style={{
                fontSize: 56,
                fontWeight: 900,
                fontFamily: 'Arial, sans-serif',
                color: '#FFFFFF',
                opacity: getWordOpacity3(index),
                transform: `scale(${getWordScale3(index)})`,
                textShadow: '0 0 25px rgba(0, 255, 255, 1), 0 0 50px rgba(0, 128, 255, 0.8)',
                display: 'inline-block',
              }}
            >
              {word}
            </span>
          ))}
        </div>
      </Sequence>
    </AbsoluteFill>
  );
};