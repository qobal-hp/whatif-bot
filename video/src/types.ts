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

export type OverlayProps = {
  type: 'message' | 'transfer';
  start: number;
  end: number;
  from?: string;
  to?: string;
  text?: string;
  amount?: string;
  date?: string;
};

export type EpisodeProps = {
  fps: number;
  durationSec: number;
  audio: string;
  scenes: SceneProps[];
  words: WordProps[];
  audioStart?: number;
  title?: string;
  music?: {src: string; start: number; end: number; volume: number}[];
  overlays?: OverlayProps[];
};
