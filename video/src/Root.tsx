import React from 'react';
import {Composition} from 'remotion';
import {Episode} from './Episode';
import type {EpisodeProps} from './types';

const empty: EpisodeProps = {fps: 30, durationSec: 5, audio: '', scenes: [], words: []};

export const Root: React.FC = () => (
  <Composition
    id="Episode"
    component={Episode}
    width={1920}
    height={1080}
    fps={30}
    durationInFrames={150}
    defaultProps={empty}
    calculateMetadata={({props}) => ({
      fps: props.fps,
      durationInFrames: Math.max(1, Math.ceil(props.durationSec * props.fps)),
    })}
  />
);
