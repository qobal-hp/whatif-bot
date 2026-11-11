import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {WordProps} from './types';

type Line = {words: WordProps[]; start: number; end: number};

const MAX_WORDS = 5;
const MAX_CHARS = 30;

const buildLines = (words: WordProps[]): Line[] => {
  const lines: Line[] = [];
  let current: WordProps[] = [];
  const flush = () => {
    if (current.length) {
      lines.push({words: current, start: current[0].start, end: current[current.length - 1].end});
      current = [];
    }
  };
  for (const word of words) {
    const chars = current.reduce((n, w) => n + w.text.length + 1, 0) + word.text.length;
    if (current.length >= MAX_WORDS || (current.length > 0 && chars > MAX_CHARS)) {
      flush();
    }
    current.push(word);
    if (/[.!?]["')]?$/.test(word.text)) {
      flush();
    }
  }
  flush();
  // Keep a line on screen until the next one starts, but never across a long pause.
  return lines.map((line, i) => {
    const next = lines[i + 1];
    const hold = next ? Math.min(next.start, line.end + 0.6) : line.end + 0.6;
    return {...line, end: hold};
  });
};

export const Captions: React.FC<{words: WordProps[]}> = ({words}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const time = frame / fps;
  const lines = useMemo(() => buildLines(words), [words]);
  const line = lines.find((l) => time >= l.start - 0.05 && time < l.end);
  if (!line) {
    return null;
  }
  const appear = interpolate(time, [line.start - 0.05, line.start + 0.12], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 96}}>
      <div
        style={{
          fontFamily: 'Montserrat, Arial, sans-serif',
          fontWeight: 800,
          fontSize: 66,
          lineHeight: 1.2,
          letterSpacing: 0.5,
          textAlign: 'center',
          maxWidth: 1500,
          opacity: appear,
          transform: `translateY(${(1 - appear) * 14}px)`,
          textShadow: '0 4px 18px rgba(0,0,0,0.9), 0 0 4px rgba(0,0,0,0.9)',
        }}
      >
        {line.words.map((word, i) => {
          const spoken = time >= word.start;
          const active = spoken && time < word.end;
          return (
            <span
              key={`${word.start}-${i}`}
              style={{
                color: active ? '#FFD34D' : spoken ? '#FFFFFF' : 'rgba(255,255,255,0.55)',
                margin: '0 0.17em',
                display: 'inline-block',
              }}
            >
              {word.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
