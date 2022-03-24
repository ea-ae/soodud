"""Product title text analysis."""

import regex
from unidecode import unidecode
import itertools as it
from typing import Iterable, NamedTuple, Sequence, Optional


COMMON_WORDS = ('ja',)

UNITS = ('mg', 'cg', 'dg', 'g', 'kg', 'ml', 'cl', 'dl', 'l', 'kl', 'mm', 'cm', 'dm', 'm', 'km', 'tk', '%')

QUANTITY_UNITS = ('g', 'l', 'm')
QUANTITY_WEIGHTS = {'m': 1 / 1000, 'c': 1 / 100, 'd': 1 / 10, 'k': 1000, '': 1}  # '' must be last for regex!
QUANTITY_SPECIAL = ('tk', 'rl', 'kmpl')


Text = NamedTuple('Text', id=int, tokens=Sequence[str], quantity=Optional[tuple[int, str]])  # original=str


def prepare_store(store: dict) -> list[Text]:
    """Prepare all products of a store."""
    # selver = {line[0] for line in csv.reader(open('selver.csv', 'r', encoding='utf-8'))}
    # coop = {line[0] for line in csv.reader(open('coop.csv', 'r', encoding='utf-8'))}

    results: list[Text] = []
    for product in store:
        result = prepare(product['name'])
        if result is None:
            continue
        tokens, _ = result

        quantity = None
        if (parse_result := parse_quantity(tokens)) is not None:
            tokens = parse_result[0]
            quantity = parse_result[1:]

        text_record = Text(product['id'], tokens, quantity)
        results.append(text_record)
        # print(text_record)
    return results


def prepare(text: str):
    """Prepares text through tokenization, transformation, normalization, and filtering."""
    original_text = text

    # replace special characters
    text = regex.sub(r'\u00B4|\u24C7|`|"|\'|\+', '', text.lower())
    text = regex.sub(r'\u00D7|\+|&|\(|\)', ' ', text)
    text = regex.sub(r',\s*(\D)', r' \1', text)

    # remove diacritics
    text = unidecode(text)

    # transform units
    for unit in UNITS:  # for transform in zip(find, replace)
        if unit != '%':
            text = regex.sub(f'(\\D)\\s+({unit})(?:\\s|$)', r'\1 1\2', text)  # kg -> 1kg
        text += ' '
        text = text.replace(f' {unit} ', f'{unit} ')

    # normalize commas
    text = regex.sub(r'(\d+\s*),(\s*\d+)', r'\1.\2', text)

    # todo: hyphenated words, e.g. 'singi-juustupirukas'; do we separate, add, keep, multiple?

    text = regex.sub(r'(\d+)\s*(?:\*|x)\s*(\d+)(?=\s*+\D)', r'\1x\2', text)  # 3 * 5 kg -> 3x5 kg

    # tokenize the string
    tokens = []
    for token in text.split():
        if token in COMMON_WORDS:  # filter common words
            continue
        token = regex.sub(r'(?:-|,|\.|/)$', '', token)  # remove junk characters
        # token = regex.sub(r'(\d)\*(\d)', r'\1x\2', token)  # 3*5tk -> 3x5tk
        token = token.strip()

        if len(token) >= 2 or token.isdigit():  # remove 1-letter tokens
            tokens.append(token)

    return (tuple(tokens), original_text) if len(tokens) > 0 else None


def parse_quantity(tokens: Sequence[str]) -> Optional[tuple[Sequence[str], int, str]]:
    """Parses quantities from tokens and deletes quantity tokens."""
    matches, final, processed_tokens = 0, None, []

    for token in tokens:
        # quantities = '|'.join(QUANTITY_UNITS + QUANTITY_SPECIAL)
        quantities = '|'.join(f'{x}{y}' for x, y in it.product(QUANTITY_WEIGHTS.keys(), QUANTITY_UNITS))
        if regex.fullmatch(f'(\\b\\d+\\.)?\\d+({quantities})\\b', token) is not None:
            matches += 1
            if matches >= 2 and token == final:
                matches -= 1
            final = token
        else:
            processed_tokens.append(token)

    if matches >= 2 or final is None:
        return None

    unit = final[-1]
    i, quantifier = (-1, '') if final[-2].isdigit() else (-2, final[-2])
    amount = float(final[:i]) * QUANTITY_WEIGHTS[quantifier]
    return processed_tokens, amount, unit


def token_equality_check(a: Text, b: Text) -> float:
    """Checks for entirely equal tokens. Very rudimentary."""
    lengths = (len(a.tokens), len(b.tokens))
    matches = len(set(a.tokens) & set(b.tokens))
    length = min(lengths) if min(lengths) >= 4 else max(lengths)  # 'Aura apple juice 0.5L' vs 'Apple'

    if length >= 6:
        return matches / length
    else:  # demand more accuracy for short names (todo: detect brand names? caps lock etc)
        return (matches / length) ** 2


def similarity_check(a: Sequence[str], b: Sequence[str]) -> float:
    """Performs similary checks on two token sequences (combining multiple similarity check algorithms).

    Different stores have differing naming formats, meaning that certain store crossovers will tend to have
    higher similarity scores on average. Because of this, similarities must be normalized against a whole
    set of comparisons between two stores.
    """
    return token_equality_check(a, b)


SimilarityScore = NamedTuple('SimilarityScore', score=float, id_a=int, id_b=int)


def find_matches(groups: Sequence[Sequence[Text]]) -> Iterable[SimilarityScore]:
    """Find similar texts between stores (max one element from each set per cluster)."""
    # comps, limit = 0, 100_000_000
    results: list[SimilarityScore] = []
    combinations = list(it.combinations(groups, 2))
    for i, (a_group, b_group) in enumerate(combinations):
        print(f'Processing new store combination... ({i + 1}/{len(combinations)})')
        for a in a_group:  # it.product()
            loc_results: list[SimilarityScore] = []
            for b in b_group:
                if a.quantity != b.quantity:
                    continue  # quantities do not match

                result = SimilarityScore(similarity_check(a, b), a.id, b.id)
                if result.score >= 0.8:
                    loc_results.append(result)

            # find best match(es) for A amongst B's
            if len(loc_results) == 0:
                continue
            loc_results.sort(key=lambda x: x.score, reverse=True)
            if len(loc_results) == 1 or loc_results[0].score != loc_results[1]:
                results.append(loc_results[0])  # multiple equal strength matches = all bad!

    results.sort(key=lambda x: -x.score)
    print('Storing results...')
    yield from results


if __name__ == '__main__':
    SAMPLE = True

    if SAMPLE:
        sample = 'Aktivia Kirsi jogurt 2.6% 4*120g'
        result = prepare(sample)
        print(' '.join(result[0]))
        quantity = parse_quantity(result[0])
        print(quantity)
    # else:
        # groups = prepare_all()
        # find_clusters(groups)
