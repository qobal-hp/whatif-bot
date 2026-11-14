export type SceneProps = {
  id: string;
  start: number;
  end: number;
  image: string;
  cut: 'fade' | 'hard';
  video?: string;
  videoSeconds?: number;
  tall?: boolean;
};

export type WordProps = {text: string; start: number; end: number};

export type OverlayProps = {
  type: 'message' | 'transfer' | 'letter' | 'text' | 'countdown';
  start: number;
  end: number;
  from?: string;
  to?: string;
  text?: string;
  amount?: string;
  date?: string;
  side?: 'left' | 'right';
  mode?: 'spoken' | 'live';
  ticks?: [number, number][];
  start_value?: number;
  color?: string;
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
  sfx?: {src: string; start: number; volume: number}[];
  ambience?: {src: string; start: number; end: number; volume: number}[];
};
