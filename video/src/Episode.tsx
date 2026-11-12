import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useVideoConfig} from 'remotion';
import '@fontsource/montserrat/800.css';
import {Captions} from './Captions';
import {Scene} from './Scene';
import type {EpisodeProps} from './types';

const FADE_FRAMES = 14;

export const Episode: React.FC<EpisodeProps> = ({audio, scenes, words, audioStart, title, durationSec, music}) => {
  const {fps, width, height} = useVideoConfig();
  const vertical = height > width;
  return (
    <AbsoluteFill style={{backgroundColor: 'black'}}>
      {scenes.map((scene, i) => {
        const fade = i > 0 && scene.cut !== 'hard' ? FADE_FRAMES : 0;
        const from = Math.round(scene.start * fps) - fade;
        // Hold each scene under the next one's fade-in so there is never a black gap.
        const duration = Math.round(scene.end * fps) - from + FADE_FRAMES;
        return (
          <Sequence key={scene.id} from={Math.max(0, from)} durationInFrames={duration}>
            <Scene scene={scene} index={i} fadeFrames={fade} totalFrames={duration} vertical={vertical} />
          </Sequence>
        );
      })}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%), linear-gradient(to top, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 32%)',
        }}
      />
      {vertical && title ? (
        <AbsoluteFill style={{alignItems: 'center', paddingTop: 210}}>
          {title.split('|').map((line, i) => (
            <div
              key={line}
              style={{
                fontFamily: 'Montserrat, Arial, sans-serif',
                fontWeight: 800,
                fontSize: 60,
                lineHeight: 1.1,
                letterSpacing: 0.5,
                textTransform: 'uppercase',
                textAlign: 'center',
                color: i === 0 ? '#111' : '#FFFFFF',
                backgroundColor: i === 0 ? '#FFD34D' : '#E0261B',
                padding: '16px 28px',
                borderRadius: 16,
                maxWidth: 980,
                marginTop: i === 0 ? 0 : -6,
                transform: `rotate(${i === 0 ? -1.5 : 1}deg)`,
                boxShadow: '0 8px 30px rgba(0,0,0,0.65)',
              }}
            >
              {line}
            </div>
          ))}
        </AbsoluteFill>
      ) : null}
      <Captions words={words} vertical={vertical} />
      {(music ?? []).map((cue, i) => {
        // Each cue overlaps its neighbours by one second on both sides so the tracks crossfade.
        const from = Math.max(0, Math.round((cue.start - 1) * fps));
        const length = Math.max(1, Math.round((cue.end + 1) * fps) - from);
        const fadeLen = Math.min(2 * fps, Math.floor(length / 2));
        return (
          <Sequence key={i} from={from} durationInFrames={length}>
            <Audio
              src={staticFile(cue.src)}
              loop
              volume={(f) =>
                cue.volume *
                interpolate(f, [0, fadeLen, length - fadeLen, length], [0, 1, 1, 0], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                })
              }
            />
          </Sequence>
        );
      })}
      {audio ? (
        <Audio
          src={staticFile(audio)}
          startFrom={Math.round((audioStart ?? 0) * fps)}
          endAt={Math.round(((audioStart ?? 0) + durationSec) * fps)}
        />
      ) : null}
    </AbsoluteFill>
  );
};
