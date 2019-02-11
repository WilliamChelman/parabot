import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { StoreState } from './store/store.state';
import { Observable, of } from 'rxjs';
import { Vote } from './core/models/vote';
import { map, filter } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  @Select(StoreState.votes)
  votes$: Observable<Vote[]>;

  results$: Observable<BaseChartDataFormat[]>;
  view = null;
  label = 'votes';

  ngOnInit(): void {
    this.results$ = this.votes$.pipe(
      filter(votes => votes.length > 0),
      map(votes => {
        const lastVote = votes[votes.length - 1];
        return [{ name: 'paragon', value: lastVote.summary.paragon }, { name: 'renegade', value: lastVote.summary.renegade }];
      })
    );
  }
}

export type BaseChartDataFormat = {
  name: string | number | Date;
  value: number;
};
