import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import '@fontsource/montserrat/800.css';
import {Overlays} from './Overlay';
import {Captions} from './Captions';
import {Scene} from './Scene';
import type {EpisodeProps} from './types';

const FADE_FRAMES = 14;

// Closing card on a short: points viewers to the full episode on the channel.
const EndCard: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const fade = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const bob = Math.sin(frame / 5) * 14;
  const [top, ...rest] = text.split('|');
  return (
    <AbsoluteFill style={{backgroundColor: `rgba(0,0,0,${0.72 * fade})`, alignItems: 'center', justifyContent: 'center', opacity: fade}}>
      <div style={{fontFamily: 'Montserrat, Arial, sans-serif', fontWeight: 800, fontSize: 84, color: '#FFD34D', textAlign: 'center', textTransform: 'uppercase', lineHeight: 1.05, maxWidth: 960, textShadow: '0 6px 30px rgba(0,0,0,0.8)'}}>
        {top}
      </div>
      {rest.map((line) => (
        <div key={line} style={{fontFamily: 'Montserrat, Arial, sans-serif', fontWeight: 800, fontSize: 64, color: '#FFFFFF', textAlign: 'center', textTransform: 'uppercase', marginTop: 24, padding: '14px 30px', backgroundColor: '#E0261B', borderRadius: 16, transform: 'rotate(-1.5deg)'}}>
          {line}
        </div>
      ))}
      <div style={{marginTop: 60, transform: `translateY(${bob}px)`, width: 0, height: 0, borderLeft: '70px solid transparent', borderRight: '70px solid transparent', borderTop: '90px solid #FFD34D'}} />
    </AbsoluteFill>
  );
};

export const Episode: React.FC<EpisodeProps> = ({audio, scenes, words, audioStart, title, durationSec, music, overlays, sfx, endCard, endCardSec}) => {
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
      <Overlays overlays={overlays ?? []} />
      {endCard ? (
        <Sequence from={Math.round((durationSec - (endCardSec ?? 3)) * fps)}>
          <EndCard text={endCard} />
        </Sequence>
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
      {(sfx ?? []).map((s, i) => (
        <Sequence key={`sfx${i}`} from={Math.round(s.start * fps)}>
          <Audio src={staticFile(s.src)} volume={s.volume} />
        </Sequence>
      ))}
      {audio ? (
        <Audio
          src={staticFile(audio)}
          startFrom={Math.round((audioStart ?? 0) * fps)}
          endAt={Math.round(((audioStart ?? 0) + durationSec - (endCard ? endCardSec ?? 3 : 0)) * fps)}
        />
      ) : null}
    </AbsoluteFill>
  );
};
