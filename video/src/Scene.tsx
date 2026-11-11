import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from './types';

type Props = {scene: SceneProps; index: number; fadeFrames: number; totalFrames: number; vertical?: boolean};

// Slow push/pull with a slight drift, alternating per scene so cuts never repeat the same move.
const MOVES = [
  {from: 1.04, to: 1.16, x: -1.2, y: -0.6},
  {from: 1.16, to: 1.05, x: 1.0, y: 0.4},
  {from: 1.05, to: 1.15, x: 0.8, y: -0.8},
  {from: 1.15, to: 1.04, x: -0.8, y: 0.6},
];

export const Scene: React.FC<Props> = ({scene, index, fadeFrames, totalFrames, vertical}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const opacity =
    fadeFrames > 0
      ? interpolate(frame, [0, fadeFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
      : 1;
  const fill: React.CSSProperties = {width: '100%', height: '100%', objectFit: 'cover'};

  if (scene.video && scene.videoSeconds) {
    // Slow the clip just enough to cover the whole scene.
    const rate = Math.min(1, Math.max(0.4, (scene.videoSeconds * fps) / totalFrames));
    return (
      <AbsoluteFill style={{opacity}}>
        <OffthreadVideo src={staticFile(scene.video)} muted playbackRate={rate} style={fill} />
      </AbsoluteFill>
    );
  }

  const move = MOVES[index % MOVES.length];
  const t = interpolate(frame, [0, totalFrames], [0, 1], {extrapolateRight: 'clamp'});
  const scale = move.from + (move.to - move.from) * t;
  if (vertical) {
    // A wide image in a tall frame: fill the height and drift sideways across it.
    const fromX = index % 2 === 0 ? 38 : 62;
    const pos = fromX + (100 - 2 * fromX) * t;
    return (
      <AbsoluteFill style={{opacity}}>
        <Img
          src={staticFile(scene.image)}
          style={{...fill, objectPosition: `${pos}% 50%`, transform: `scale(${1 + 0.06 * t})`}}
        />
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{opacity}}>
      <Img
        src={staticFile(scene.image)}
        style={{
          ...fill,
          transform: `scale(${scale}) translate(${move.x * t}%, ${move.y * t}%)`,
        }}
      />
    </AbsoluteFill>
  );
};
