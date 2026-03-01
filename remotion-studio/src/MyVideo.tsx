import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Sequence, Easing } from 'remotion';

const LogoSVG: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 400 400">
    <defs>
      <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#00d4ff" />
        <stop offset="50%" stopColor="#7b2ff7" />
        <stop offset="100%" stopColor="#f107a3" />
      </linearGradient>
    </defs>
    <rect x="50" y="50" width="300" height="300" rx="40" fill="url(#logoGradient)" />
    <text x="200" y="220" textAnchor="middle" fill="#ffffff" fontSize="48" fontWeight="bold" fontFamily="Arial, sans-serif">CYBER</text>
    <text x="200" y="280" textAnchor="middle" fill="#ffffff" fontSize="32" fontWeight="300" fontFamily="Arial, sans-serif">BRAND</text>
  </svg>
);

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const phaseAEnd = 5 * fps; // 300 frames
  const phaseBEnd = 15 * fps; // 900 frames
  const phaseCEnd = 20 * fps; // 1200 frames
  const logoSize = 400;

  const glitchOpacity = interpolate(frame, [0, phaseAEnd], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.25, 0.1, 0.25, 1) });

  const phaseBFrame = Math.max(0, frame - phaseAEnd);
  const phaseBDuration = phaseBEnd - phaseAEnd;
  const rotateY = interpolate(phaseBFrame, [0, phaseBDuration], [-45, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const rotateX = interpolate(phaseBFrame, [0, phaseBDuration], [20, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const sheenX = interpolate(phaseBFrame, [0, phaseBDuration], [-100, 200], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  const phaseCFrame = Math.max(0, frame - phaseBEnd);
  const phaseCDuration = phaseCEnd - phaseBEnd;
  const springScale = spring({ frame: phaseCFrame, fps, config: { damping: 30, stiffness: 100 } });
  const shakeX = interpolate(phaseCFrame, [0, 15, 30], [0, 5, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const shakeY = interpolate(phaseCFrame, [0, 15, 30], [0, -5, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const textOpacity = interpolate(phaseCFrame, [0, 60], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  const fadeOut = interpolate(frame, [1140, 1200], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a1a', justifyContent: 'center', alignItems: 'center', overflow: 'hidden' }}>
      <div style={{ position: 'absolute', inset: 0, backgroundImage: `linear-gradient(135deg, #050505 0%, #1a1a2e 100%), linear-gradient(rgba(20, 20, 40, 0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(20, 20, 40, 0.5) 1px, transparent 1px)`, backgroundSize: '100% 100%, 50px 50px, 50px 50px', opacity: 0.8 }} />

      <Sequence from={0} durationInFrames={phaseBEnd}>
        <div style={{ perspective: '1000px', transformStyle: 'preserve-3d', width: logoSize, height: logoSize, position: 'relative' }}>
          {[0, 1, 2, 3, 4].map((i) => (
            <div key={i} style={{ position: 'absolute', top: 0, left: 0, width: logoSize, height: logoSize, transform: `translateZ(${-i}px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`, transformStyle: 'preserve-3d', zIndex: 5 - i, opacity: glitchOpacity * (i === 0 ? 1 : 0.3), filter: i === 0 ? 'none' : 'brightness(0.3)' }}>
              <LogoSVG size={logoSize} />
            </div>
          ))}
          <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.4) 50%, transparent 100%)', transform: `translateX(${sheenX}%) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`, mixBlendMode: 'overlay', pointerEvents: 'none' }} />
        </div>
      </Sequence>

      <Sequence from={phaseBEnd} durationInFrames={phaseCDuration}>
        <div style={{ transform: `scale(${springScale}) translateX(${shakeX}px) translateY(${shakeY}px)` }}>
          <LogoSVG size={logoSize} />
          <div style={{ marginTop: 40, textAlign: 'center', opacity: textOpacity }}>
            <span style={{ fontFamily: 'Arial, sans-serif', fontSize: 48, fontWeight: 'bold', color: '#ffffff', letterSpacing: '10px', textTransform: 'uppercase' }}>OFFICIAL CHANNEL</span>
          </div>
        </div>
      </Sequence>

      <AbsoluteFill style={{ backgroundColor: '#000000', opacity: 1 - fadeOut, pointerEvents: 'none' }} />
    </AbsoluteFill>
  );
};
