"""Product title text analysis."""

import regex
from unidecode import unidecode
from collections import Counter
import itertools as it
from typing import Iterable, NamedTuple, Sequence, Optional


BLACKLIST = ('ja', 'hulgi', 'rimi', 'coop', 'selver', 'selveri pagarid', 'selveri köök', 'coop kokad')
WHITELIST = ()

UNITS = ('mg', 'cg', 'dg', 'g', 'kg', 'ml', 'cl', 'dl', 'l', 'kl', 'mm', 'cm', 'dm', 'm', 'km', 'tk', '%')

QUANTITY_UNITS = ('g', 'l', 'm')
QUANTITY_WEIGHTS = {'m': 1 / 1000, 'c': 1 / 100, 'd': 1 / 10, 'k': 1000, '': 1}  # '' must be last for regex!
QUANTITY_SPECIAL = ('%', 'tk')  # rl, kmpl


Quantity = NamedTuple('Quantity', amount=int, unit=str)
Text = NamedTuple('Text', id=int, tokens=Sequence[str], quantity=Sequence[Quantity])  # original=str


ratios = {}


def prepare_store(store: dict) -> list[Text]:
    """Prepare all products of a store."""
    results: list[Text] = []
    counter, tokens_total = Counter(), 0
    for product in store:
        result = prepare(product['name'])
        if result is None:
            continue
        tokens, _ = result

        quantities = set()
        if (parse_result := parse_quantity(tokens)) is not None:
            tokens = parse_result[0]
            quantities = parse_result[1:]

        counter.update(tokens)
        tokens_total += len(tokens)

        text_record = Text(product['id'], tokens, quantities)
        results.append(text_record)
    for k, v in counter.items():
        ratios.setdefault(k, []).append(v / tokens_total)

    real_ratios = {k: sum(v) / 3 for k, v in ratios.items()}
    real_ratios = sorted(real_ratios.items(), key=lambda it: -it[1])[:300]
    hi = max(real_ratios, key=lambda r: r[1])[1]
    for k, v in real_ratios[::-1]:
        print(f'{k}: {v / hi:.2%}', end=' | ')
    print()

    return results


def prepare(text: str) -> Optional[tuple[list[str], str]]:
    """Prepares text through tokenization, transformation, normalization, and filtering."""
    original_text = text

    # replace special characters
    text = regex.sub(r'\u00B4|\u24C7|`|"|\'|\+', '', text.lower())
    text = regex.sub(r'\u00D7|\+|&|\(|\)', ' ', text)
    text = regex.sub(r',\s*(\D)', r' \1', text)

    text = unidecode(text)  # remove diacritics

    # transform units
    for unit in UNITS:  # for transform in zip(find, replace)
        if unit != '%':
            text = regex.sub(f'(\\D)\\s+({unit})(?:\\s|$)', r'\1 1\2', text)  # kg -> 1kg
        text += ' '
        text = text.replace(f' {unit} ', f'{unit} ')

    # todo: hyphenated words, e.g. 'singi-juustupirukas'; do we separate, add, keep, multiple?
    text = regex.sub(r'(\d+\s*),(\s*\d+)', r'\1.\2', text)  # normalize commas
    text = regex.sub(r'(\d+)\s*(?:\*|x)\s*(\d+)(?=\s*+\D)', r'\1x\2', text)  # 3 * 5 kg -> 3x5 kg

    for blacklist_item in BLACKLIST:  # get rid of junk words
        for whitelist_item in WHITELIST:  # unless they are part of a brand name, etc
            if blacklist_item in whitelist_item:
                break
        else:
            text = regex.sub(f'\\b{blacklist_item}\\b', '', text)

    # tokenize the string
    tokens = []
    for token in text.split():
        token = regex.sub(r'(?:-|,|\.|/)$', '', token)  # remove junk characters
        token = token.strip()

        if len(token) >= 2 or token.isdigit():  # remove 1-letter tokens
            tokens.append(token)

    return (tuple(tokens), original_text) if len(tokens) > 0 else None


def parse_quantity(tokens: Sequence[str]) -> Optional[tuple[list[str], set[Quantity]]]:
    """Parses quantities from tokens and deletes quantity tokens."""
    quantities, processed_tokens = set(), []

    for token in tokens:
        # quantities = '|'.join(QUANTITY_UNITS + QUANTITY_SPECIAL)
        units = '|'.join(f'{w}{q}' for w, q in it.product(QUANTITY_WEIGHTS.keys(), QUANTITY_UNITS))
        units += '|' + '|'.join(q for q in QUANTITY_SPECIAL)

        if (match := regex.fullmatch(f'(\\b\\d+\\.)?\\d+(?P<u>{units})($|\\s)', token)) is not None:
            unit = match.group('u')
            i, quantifier = -len(unit), unit[0] if len(unit) == 2 else ''
            amount = float(token[:i]) if unit in QUANTITY_SPECIAL else float(token[:i]) * QUANTITY_WEIGHTS[quantifier]
            base_unit = unit if unit in QUANTITY_SPECIAL else unit.replace(quantifier, '')
            quantities.add(Quantity(amount, base_unit))
        else:
            processed_tokens.append(token)

    return processed_tokens, quantities if len(processed_tokens) > 0 else None


def token_equality_check(a: Text, b: Text) -> float:
    """Checks for entirely equal tokens. Very rudimentary."""
    lengths = (len(a.tokens), len(b.tokens))
    matches = len(set(a.tokens) & set(b.tokens))
    length = min(lengths) if min(lengths) >= 4 else max(lengths)  # 'Aura apple juice 0.5L' vs 'Apple'

    if length >= 6:
        return matches / length
    else:  # demand more accuracy for short names (todo: detect brand names? caps lock etc)
        return (matches / length) ** 2


def similarity_check(a: Text, b: Text) -> float:
    """Performs similary checks on two token sequences (combining multiple similarity check algorithms).

    Different stores have differing naming formats, meaning that certain store crossovers will tend to have
    higher similarity scores on average. Because of this, similarities must be normalized against a whole
    set of comparisons between two stores.
    """
    if a.quantity != b.quantity:
        return 0
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
        sample = 'Minu rimi toode 37.5 % 0.5l'
        result = prepare(sample)
        print(' '.join(result[0]))
        quantity = parse_quantity(result[0])
        print(quantity)
    # else:
        # groups = prepare_all()
        # find_clusters(groups)
