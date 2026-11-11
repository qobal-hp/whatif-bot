import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import '@fontsource/montserrat/800.css';
import {Captions} from './Captions';
import {Scene} from './Scene';
import type {EpisodeProps} from './types';

const FADE_FRAMES = 14;

export const Episode: React.FC<EpisodeProps> = ({audio, scenes, words}) => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: 'black'}}>
      {scenes.map((scene, i) => {
        const fade = i > 0 && scene.cut !== 'hard' ? FADE_FRAMES : 0;
        const from = Math.round(scene.start * fps) - fade;
        // Hold each scene under the next one's fade-in so there is never a black gap.
        const duration = Math.round(scene.end * fps) - from + FADE_FRAMES;
        return (
          <Sequence key={scene.id} from={Math.max(0, from)} durationInFrames={duration}>
            <Scene scene={scene} index={i} fadeFrames={fade} totalFrames={duration} />
          </Sequence>
        );
      })}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%), linear-gradient(to top, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 32%)',
        }}
      />
      <Captions words={words} />
      {audio ? <Audio src={staticFile(audio)} /> : null}
    </AbsoluteFill>
  );
};
