import React from 'react';
import {Composition} from 'remotion';
import {Episode} from './Episode';
import {Thumb} from './Thumb';
import type {EpisodeProps} from './types';

const empty: EpisodeProps = {fps: 30, durationSec: 5, audio: '', scenes: [], words: []};

const meta = ({props}: {props: EpisodeProps}) => ({
  fps: props.fps,
  durationInFrames: Math.max(1, Math.ceil(props.durationSec * props.fps)),
});

export const Root: React.FC = () => (
  <>
  <Composition
    id="Episode"
    component={Episode}
    width={1920}
    height={1080}
    fps={30}
    durationInFrames={150}
    defaultProps={empty}
    calculateMetadata={meta}
  />
  <Composition
    id="Short"
    component={Episode}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={150}
    defaultProps={empty}
    calculateMetadata={meta}
  />
  <Composition
    id="Thumb"
    component={Thumb}
    width={1280}
    height={720}
    fps={30}
    durationInFrames={1}
    defaultProps={{image: '', side: 'left' as const, lines: [], tag: ''}}
  />
  </>
);
