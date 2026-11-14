import React from 'react';
import {AbsoluteFill, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {OverlayProps} from './types';

const font = 'Montserrat, Arial, sans-serif';

const Card: React.FC<{children: React.ReactNode; length: number; side?: 'left' | 'right'}> = ({children, length, side}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame, fps, config: {damping: 16, stiffness: 140}});
  const out = interpolate(frame, [length - 10, length], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: `rgba(0,0,0,${0.45 * out})`, justifyContent: 'center', alignItems: side === 'left' ? 'flex-start' : side === 'right' ? 'flex-end' : 'center', padding: '0 90px 190px'}}>
      <div style={{opacity: out, transform: `scale(${0.85 + 0.15 * pop})`, fontFamily: font}}>{children}</div>
    </AbsoluteFill>
  );
};

const Message: React.FC<{o: OverlayProps}> = ({o}) => (
  <div style={{width: 980, backgroundColor: '#0f1115', borderRadius: 36, padding: '34px 40px 44px', boxShadow: '0 30px 90px rgba(0,0,0,0.8)', border: '2px solid #2a2e37'}}>
    <div style={{display: 'flex', alignItems: 'center', gap: 20, marginBottom: 30}}>
      <div style={{width: 72, height: 72, borderRadius: 36, backgroundColor: '#3a4150', color: '#fff', fontSize: 36, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        {(o.from ?? '?').charAt(0)}
      </div>
      <div>
        <div style={{color: '#fff', fontSize: 38, fontWeight: 800}}>{o.from}</div>
        <div style={{color: '#8a93a6', fontSize: 28, fontWeight: 600}}>to {o.to}</div>
      </div>
    </div>
    <div style={{backgroundColor: '#2f7cf6', color: '#fff', fontSize: 50, fontWeight: 600, lineHeight: 1.25, padding: '28px 34px', borderRadius: '34px 34px 34px 8px'}}>{o.text}</div>
  </div>
);

const Transfer: React.FC<{o: OverlayProps}> = ({o}) => (
  <div style={{width: 980, backgroundColor: '#f6f4ee', borderRadius: 24, padding: '40px 48px', boxShadow: '0 30px 90px rgba(0,0,0,0.8)', color: '#15171c'}}>
    <div style={{fontSize: 30, fontWeight: 800, letterSpacing: 4, color: '#6b7280'}}>WIRE TRANSFER CONFIRMATION</div>
    <div style={{fontSize: 104, fontWeight: 800, margin: '14px 0 26px', color: '#b3261e'}}>{o.amount}</div>
    {[
      ['FROM', o.from],
      ['TO', o.to],
      ['SENT', o.date],
    ].map(([label, value]) => (
      <div key={label} style={{display: 'flex', borderTop: '2px solid #d9d5c8', padding: '18px 0', fontSize: 40}}>
        <div style={{width: 170, fontWeight: 800, color: '#6b7280'}}>{label}</div>
        <div style={{fontWeight: 800}}>{value}</div>
      </div>
    ))}
  </div>
);

const Letter: React.FC<{o: OverlayProps}> = ({o}) => (
  <div style={{width: 1040, backgroundColor: '#f3ead7', borderRadius: 6, padding: '56px 64px', boxShadow: '0 30px 90px rgba(0,0,0,0.8)', color: '#2b2118', fontFamily: 'Georgia, serif', fontStyle: 'italic', fontSize: 52, lineHeight: 1.4}}>
    {o.text}
  </div>
);

// A closing question in big type, for the end of a short.
const Text: React.FC<{o: OverlayProps}> = ({o}) => (
  <div style={{width: 940, textAlign: 'center', color: '#fff', fontSize: 104, fontWeight: 900, lineHeight: 1.1, textTransform: 'uppercase', textShadow: '0 8px 40px rgba(0,0,0,0.9)'}}>
    {(o.text ?? '').split('|').map((line, i) => (
      <div key={i} style={{color: i === 0 ? '#fff' : '#ffd400'}}>{line}</div>
    ))}
  </div>
);

const two = (n: number) => String(Math.max(0, Math.floor(n))).padStart(2, '0');

// A glowing digital countdown floating at the top of the frame.
const Countdown: React.FC<{o: OverlayProps}> = ({o}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const now = o.start + frame / fps;
  let value = o.start_value ?? 0;
  if (o.mode === 'live') {
    value = Math.max(0, (o.start_value ?? 0) - frame / fps);
  } else {
    const past = (o.ticks ?? []).filter(([t]) => t <= now);
    value = past.length ? past[past.length - 1][1] : (o.start_value ?? (o.ticks?.[0]?.[1] ?? 0));
  }
  const color = o.color ?? '#ff2a2a';
  const zero = value <= 0;
  const pulse = 0.75 + 0.25 * Math.sin((frame / fps) * Math.PI * 2);
  const text = `${two(value / 3600)}:${two((value % 3600) / 60)}:${two(value % 60)}`;
  const size = Math.round(Math.min(width, height * 1.6) * 0.085);
  const fadeIn = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'flex-start', paddingTop: height > width ? 470 : 70, opacity: fadeIn}}>
      <div style={{fontFamily: '"Courier New", monospace', fontWeight: 800, fontSize: size, letterSpacing: size * 0.08, color: zero ? '#ffffff' : color, padding: `${size * 0.12}px ${size * 0.35}px`, border: `4px solid ${color}`, borderRadius: 18, backgroundColor: 'rgba(20,0,0,0.55)', textShadow: `0 0 ${18 * pulse}px ${color}, 0 0 ${42 * pulse}px ${color}`, boxShadow: `0 0 ${40 * pulse}px ${color}`}}>
        {text}
      </div>
    </AbsoluteFill>
  );
};

export const Overlays: React.FC<{overlays: OverlayProps[]}> = ({overlays}) => {
  const {fps} = useVideoConfig();
  return (
    <>
      {overlays.map((o, i) => {
        const from = Math.round(o.start * fps);
        const length = Math.max(1, Math.round((o.end - o.start) * fps));
        return (
          <Sequence key={i} from={from} durationInFrames={length}>
            {o.type === 'countdown' ? <Countdown o={o} /> : <Card length={length} side={o.side}>{o.type === 'transfer' ? <Transfer o={o} /> : o.type === 'letter' ? <Letter o={o} /> : o.type === 'text' ? <Text o={o} /> : <Message o={o} />}</Card>}
          </Sequence>
        );
      })}
    </>
  );
};
