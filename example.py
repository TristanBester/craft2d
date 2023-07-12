import time
from collections import defaultdict

import numpy as np
from tqdm import tqdm

from craft2d.env.environment import Craft2dEnv

TASK = "get-wood"


def get_rep(o):
    return tuple(
        (
            tuple(o[0].flatten()),
            # tuple(np.array([0, 0, 0]).flatten()),
            tuple(o[1].flatten()),
            tuple(o[2].flatten()),
        )
    )


def eval(Q, env):
    done = False
    o = env.reset(task=TASK)

    for t in range(30):
        if done:
            break

        a = np.argmax(Q[get_rep(o)])
        o_prime, r, done = env.step(a)

        o = o_prime
    return r


def render_eval(Q, env):
    done = False
    o = env.reset(task=TASK)

    env.render()

    for t in range(30):
        if done:
            break

        a = np.argmax(Q[get_rep(o)])
        o_prime, r, done = env.step(a)

        env.render()
        time.sleep(0.5)
        o = o_prime
    return r


if __name__ == "__main__":
    Q = defaultdict(lambda: np.zeros(5))

    # env = Craft2dEnv(10, 10, render_mode=None)
    env = Craft2dEnv(10, 10, render_mode="human")

    pbar = tqdm(range(1000000))
    rewards = []
    obs_r = []

    hit_count = []

    for episode in pbar:
        o = env.reset(task=TASK)
        done = False

        # print(get_rep(o))

        # env.render()

        for t in range(5000):
            # print(get_rep(o))
            if done:
                break

            if get_rep(o) not in Q:
                hit_count.append(0)
            else:
                hit_count.append(1)

            if np.random.random() < 0.5:
                a = np.random.choice([0, 1, 2, 3, 4])
            else:
                a = np.argmax(Q[get_rep(o)])

            # a = int(input())

            o_prime, r, done = env.step(a)

            if r == 1:
                # print("Updating ", get_rep(o), a, r, Q[get_rep(o)][a])

                Q[get_rep(o)][a] += 0.01 * (r - Q[get_rep(o)][a])
            else:
                Q[get_rep(o)][a] += 0.01 * (
                    (r + 0.999 * np.max(Q[get_rep(o_prime)])) - Q[get_rep(o)][a]
                )

            o = o_prime

            # env.render()

        rewards.append(eval(Q, env))
        # rewards.append(r)
        obs_r.append(r)

        if episode % 250 == 0:
            pbar.set_description(
                f"Reward {np.mean(rewards[-100:])}, {np.mean(obs_r[-100:])}, {np.mean(hit_count[-1000:])}"
            )
        if episode % 10000 == 0 and episode > 0:
            render_eval(Q, env)
