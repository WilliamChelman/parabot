import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Vote } from '../models/vote';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VoteService {
  private url = '/votes';

  private fakeVotes: Vote[] = [];

  constructor(private http: HttpClient) {}

  getVotes(): Observable<Vote[]> {
    // return this.http.get<Vote[]>(this.url);
    const paragon = generateRandomNumber(1000);
    const renegade = generateRandomNumber(1000);

    this.fakeVotes = [
      ...(this.fakeVotes.length < 100 ? this.fakeVotes : []),
      {
        timestamp: Date.now(),
        last_vote: {
          voter: 'voter' + this.fakeVotes.length,
          alignment_changes: Math.random() > 0.5,
          vote: Math.random() > 0.5 ? 'paragon' : 'renegade'
        },
        summary: {
          alignment: Math.random() > 0.5 ? 'paragon' : 'renegade',
          paragon,
          renegade,
          renegade_perc: renegade / (renegade + paragon)
        }
      }
    ];
    return of(this.fakeVotes);
  }

  getId(vote: Vote): string {
    return `${vote.timestamp}-${vote.last_vote.voter}`;
  }
}

function generateRandomNumber(max: number, min: number = 0): number {
  return Math.random() * (max - min) + min;
}
