export type Alignment = 'renegade' | 'paragon';

export interface Vote {
  timestamp: number;
  last_vote: {
    voter: string;
    vote: Alignment;
    alignment_changes: boolean;
  };
  summary: {
    renegade_perc: number;
    renegade: number;
    paragon: number;
    alignment: Alignment;
  };
}
