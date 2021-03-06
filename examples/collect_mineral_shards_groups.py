import numpy as np

from examples.base_example import BaseExample

__author__ = 'Islam Elnabarawy'

_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals

_ENV_NAME = "SC2CollectMineralShards-v2"
_VISUALIZE = False
_STEP_MUL = None
_NUM_EPISODES = 10


class CollectMineralShardsGroups(BaseExample):
    def __init__(self, visualize=False, step_mul=None) -> None:
        super().__init__(_ENV_NAME, visualize, step_mul)
        self.next_group = 0

    def get_action(self, env, obs):
        neutral_y, neutral_x = (obs[0] == _PLAYER_NEUTRAL).nonzero()
        marine_y, marine_x = ((obs[0] == _PLAYER_FRIENDLY) - obs[1]).nonzero()
        if not neutral_y.any():
            raise Exception('No minerals found!')
        if not marine_y.any():
            marine_y, marine_x, _ = obs[1].nonzero()
        if not marine_y.any():
            raise Exception('No marines found!')
        marine = [np.ceil(marine_x.mean()).astype(int), np.ceil(marine_y.mean()).astype(int)]
        shards = np.array(list(zip(neutral_x, neutral_y)))
        closest_ix = np.argmin(np.linalg.norm(np.array(marine) - shards, axis=1))
        target = shards[closest_ix].tolist()
        group = [self.next_group + 1]
        self.next_group = (self.next_group + 1) % 2
        return group + target


def main():
    example = CollectMineralShardsGroups(_VISUALIZE, _STEP_MUL)
    rewards = example.run(_NUM_EPISODES)
    print('Total reward: {}'.format(rewards.sum()))
    print('Average reward: {} +/- {}'.format(rewards.mean(), rewards.std()))
    print('Minimum reward: {}'.format(rewards.min()))
    print('Maximum reward: {}'.format(rewards.max()))


if __name__ == "__main__":
    main()
