import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import '@fontsource/montserrat/800.css';
import {Captions} from './Captions';
import {Scene} from './Scene';
import type {EpisodeProps} from './types';

const FADE_FRAMES = 14;

export const Episode: React.FC<EpisodeProps> = ({audio, scenes, words, audioStart, title, durationSec}) => {
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
        <AbsoluteFill style={{alignItems: 'center', paddingTop: 230}}>
          <div
            style={{
              fontFamily: 'Montserrat, Arial, sans-serif',
              fontWeight: 800,
              fontSize: 46,
              lineHeight: 1.15,
              letterSpacing: 1,
              textTransform: 'uppercase',
              textAlign: 'center',
              color: '#111',
              backgroundColor: '#FFD34D',
              padding: '18px 30px',
              borderRadius: 18,
              maxWidth: 880,
              boxShadow: '0 8px 30px rgba(0,0,0,0.6)',
            }}
          >
            {title}
          </div>
        </AbsoluteFill>
      ) : null}
      <Captions words={words} vertical={vertical} />
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
