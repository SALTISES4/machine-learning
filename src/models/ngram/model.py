from functools import partial, reduce
from math import exp, log
from operator import mul
from typing import Dict

from .data import read_data


def create_model(language: str, max_gram: int = 3):
    data = {
        gram: val
        for gram, val in read_data(language).items()
        if gram <= max_gram
    }
    return partial(predict, data=data)


def predict(text: str, data: Dict[int, Dict[str, float]]) -> float:
    random = {
        gram: {g: 1 / len(val) for g in val.keys()}
        for gram, val in data.items()
    }

    l1 = log_likelihood(text, data)
    l0 = log_likelihood(text, random)

    return 1 - min(1, exp(l0 - l1))


def likelihood(text: str, ngrams: Dict[int, Dict[str, float]]) -> float:
    text = "".join(c for c in text.lower() if c == " " or c in ngrams[1])
    words = [
        [c for c in word.lower() if c in ngrams[1]] for word in text.split()
    ]

    if len(ngrams) == 1:
        return reduce(
            mul,
            (
                reduce(mul, (ngrams[1][word[i]] for i in range(len(word))), 1)
                for word in words
            ),
            1,
        )
    else:
        return reduce(
            mul,
            (
                reduce(
                    mul,
                    (
                        ngrams[1][word[0]],
                        *(
                            ngrams[i]["".join(word[:i])]
                            / ngrams[i - 1]["".join(word[: i - 1])]
                            for i in range(2, min(len(ngrams), len(word) + 1))
                        ),
                        *(
                            ngrams[len(ngrams)][
                                "".join(word[i : i + len(ngrams)])
                            ]
                            / ngrams[len(ngrams) - 1][
                                "".join(word[i : i + len(ngrams) - 1])
                            ]
                            for i in range(len(word) - len(ngrams) + 1)
                        ),
                    ),
                    1,
                )
                for word in words
            ),
            1,
        )


def log_likelihood(text: str, ngrams: Dict[int, Dict[str, float]]) -> float:
    text = "".join(c for c in text.lower() if c == " " or c in ngrams[1])
    words = [
        [c for c in word.lower() if c in ngrams[1]] for word in text.split()
    ]

    if len(ngrams) == 1:
        return sum(
            sum(log(ngrams[1][word[i]]) for i in range(len(word)))
            for word in words
        )
    else:
        return sum(
            sum(
                (
                    log(ngrams[1][word[0]]),
                    *(
                        log(
                            ngrams[i]["".join(word[:i])]
                            / ngrams[i - 1]["".join(word[: i - 1])]
                        )
                        for i in range(2, min(len(ngrams), len(word) + 1))
                    ),
                    *(
                        log(
                            ngrams[len(ngrams)][
                                "".join(word[i : i + len(ngrams)])
                            ]
                            / ngrams[len(ngrams) - 1][
                                "".join(word[i : i + len(ngrams) - 1])
                            ]
                        )
                        for i in range(len(word) - len(ngrams) + 1)
                    ),
                )
            )
            for word in words
        )
