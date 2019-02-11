import { State, Action, StateContext, NgxsOnInit, Selector } from '@ngxs/store';
import { FetchVotes } from './store.actions';
import { Vote } from '../core/models/vote';
import { interval } from 'rxjs';
import { tap } from 'rxjs/operators';
import { VoteService } from '../core/services/vote.service';

export interface StoreStateModel {
  votes: Vote[];
}

@State<StoreStateModel>({
  name: 'store',
  defaults: {
    votes: []
  }
})
export class StoreState implements NgxsOnInit {
  @Selector()
  static votes(state: StoreStateModel): Vote[] {
    return state.votes;
  }

  @Action(FetchVotes)
  fetchVotes({ patchState }: StateContext<StoreStateModel>) {
    return this.voteService.getVotes().pipe(tap(votes => patchState({ votes })));
  }

  constructor(private voteService: VoteService) {}

  ngxsOnInit({ dispatch }: StateContext<StoreStateModel>) {
    dispatch(new FetchVotes());
    interval(2000).subscribe(() => dispatch(new FetchVotes()));
  }
}
