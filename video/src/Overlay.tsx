import React from 'react';
import {AbsoluteFill, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {OverlayProps} from './types';

const font = 'Montserrat, Arial, sans-serif';

const Card: React.FC<{children: React.ReactNode; length: number}> = ({children, length}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame, fps, config: {damping: 16, stiffness: 140}});
  const out = interpolate(frame, [length - 10, length], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: `rgba(0,0,0,${0.45 * out})`, justifyContent: 'center', alignItems: 'center', paddingBottom: 190}}>
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

export const Overlays: React.FC<{overlays: OverlayProps[]}> = ({overlays}) => {
  const {fps} = useVideoConfig();
  return (
    <>
      {overlays.map((o, i) => {
        const from = Math.round(o.start * fps);
        const length = Math.max(1, Math.round((o.end - o.start) * fps));
        return (
          <Sequence key={i} from={from} durationInFrames={length}>
            <Card length={length}>{o.type === 'transfer' ? <Transfer o={o} /> : <Message o={o} />}</Card>
          </Sequence>
        );
      })}
    </>
  );
};
