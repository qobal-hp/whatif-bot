export type SceneProps = {
  id: string;
  start: number;
  end: number;
  image: string;
  cut: 'fade' | 'hard';
  video?: string;
  videoSeconds?: number;
};

export type WordProps = {text: string; start: number; end: number};

export type EpisodeProps = {
  fps: number;
  durationSec: number;
  audio: string;
  scenes: SceneProps[];
  words: WordProps[];
  audioStart?: number;
  title?: string;
  music?: {src: string; start: number; end: number; volume: number}[];
};
