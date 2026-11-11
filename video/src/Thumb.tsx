import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import '@fontsource/montserrat/900.css';

export type ThumbProps = {
  image: string;
  side: 'left' | 'right';
  lines: {text: string; color: string}[];
  tag?: string;
};

const outline = '0 0 0 #000, 6px 6px 0 #000, -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 0 12px 40px rgba(0,0,0,0.9)';

export const Thumb: React.FC<ThumbProps> = ({image, side, lines, tag}) => {
  const left = side === 'left';
  return (
    <AbsoluteFill style={{backgroundColor: 'black'}}>
      {image ? <Img src={staticFile(image)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /> : null}
      <AbsoluteFill
        style={{
          background: `linear-gradient(to ${left ? 'right' : 'left'}, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.35) 38%, rgba(0,0,0,0) 62%)`,
        }}
      />
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: left ? 'flex-start' : 'flex-end',
          padding: '0 54px',
          fontFamily: 'Montserrat, Arial, sans-serif',
          fontWeight: 900,
          textAlign: left ? 'left' : 'right',
        }}
      >
        {lines.map((line) => (
          <div
            key={line.text}
            style={{
              color: line.color,
              fontSize: line.text.length > 8 ? 112 : 136,
              lineHeight: 1.02,
              letterSpacing: -2,
              textShadow: outline,
              whiteSpace: 'nowrap',
            }}
          >
            {line.text}
          </div>
        ))}
        {tag ? (
          <div
            style={{
              marginTop: 26,
              fontSize: 44,
              color: '#111',
              backgroundColor: '#FFD400',
              padding: '8px 22px',
              borderRadius: 10,
              transform: 'rotate(-2deg)',
              boxShadow: '0 8px 24px rgba(0,0,0,0.7)',
            }}
          >
            {tag}
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
