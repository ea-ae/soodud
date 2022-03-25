"""Product title text analysis."""

import regex
from unidecode import unidecode
from collections import Counter
import itertools as it
from typing import Iterable, NamedTuple, Sequence, Optional

import line_profiler
profile = line_profiler.LineProfiler()


BLACKLIST = ('ja', 'hulgi', 'rimi', 'coop', 'selver', 'selveri pagarid', 'selveri köök', 'coop kokad')
WHITELIST = ()

UNITS = ('mg', 'cg', 'dg', 'g', 'kg', 'ml', 'cl', 'dl', 'l', 'kl', 'mm', 'cm', 'dm', 'm', 'km', '%', 'tk')

QUANTITY_UNITS = ('g', 'l', 'm')
QUANTITY_WEIGHTS = {'m': 1 / 1000, 'c': 1 / 100, 'd': 1 / 10, 'k': 1000, '': 1}  # '' must be last for regex!
SI_UNITS = tuple(f'{w}{q}' for w, q in it.product(QUANTITY_WEIGHTS.keys(), QUANTITY_UNITS))
QUANTITY_SPECIAL = ('%', 'tk')  # rl, kmpl


Quantity = NamedTuple('Quantity', amount=int, unit=str)
Text = NamedTuple('Text', id=int, tokens=Sequence[str], quantity=Sequence[Quantity])  # original=str


ratios = {}


@profile
def prepare_store(store: dict) -> list[Text]:
    """Prepare all products of a store."""
    results: list[Text] = []
    counter, tokens_total = Counter(), 0
    for product in store:
        tokens = prepare(product['name'])
        if len(tokens) == 0:
            continue

        quantities = set()
        if (parse_result := parse_quantity(tokens)) is not None:
            tokens = parse_result[0]
            quantities = parse_result[1:]

        counter.update(tokens)
        tokens_total += len(tokens)

        text_record = Text(product['id'], tokens, quantities)
        results.append(text_record)

    # for k, v in counter.items():
    #     ratios.setdefault(k, []).append(v / tokens_total)
    # real_ratios = {k: sum(v) / 3 for k, v in ratios.items()}
    # real_ratios = sorted(real_ratios.items(), key=lambda it: -it[1])[:1000]
    # hi = max(real_ratios, key=lambda r: r[1])[1]
    # for k, v in real_ratios[::-1]:
    #     print(f'{k}: {v / hi:.2%}', end=' | ')
    # print()

    profile.print_stats()
    return results


@profile
def prepare(text: str) -> list[str]:
    """Prepares text through tokenization, transformation, normalization, and filtering."""
    text = regex.sub(r'\u00B4|\u24C7|`|"|\'|\+', '', text.lower())
    text = regex.sub(r'\u00D7|\+|&|\(|\)', ' ', text)
    text = regex.sub(r',\s*(\D)', r' \1', text)

    text = unidecode(text)  # remove diacritics

    # todo: hyphenated words, e.g. 'singi-juustupirukas'; do we separate, add, keep, multiple?
    text = regex.sub(r'(\d+\s*),(\s*\d+)', r'\1.\2', text)  # normalize commas
    text = regex.sub(r'(\d+)\s*(?:\*|x)\s*(\d+)(?=\s*+\D)', r'\1x\2', text)  # 3 * 5 kg -> 3x5 kg

    for blacklist_item in BLACKLIST:  # get rid of junk words
        for whitelist_item in WHITELIST:  # unless they are part of a brand name, etc
            if blacklist_item in whitelist_item:
                break
        else:
            text = (' ' + text + ' ').replace(blacklist_item, '')

    # tokenize the string
    tokens = []
    for token in text.split():
        token = regex.sub(r'(?:-|,|!|\.|/)$', '', token)  # remove junk characters
        token = token.strip()

        if token in UNITS:
            if len(tokens) > 0 and tokens[-1].replace('.', '').isdigit():
                tokens[-1] = tokens[-1] + token  # 3 tk -> 3tk
                continue
            elif token not in QUANTITY_SPECIAL:
                token = '1' + token  # kg -> 1kg

        if len(token) >= 2 or token.isdigit():  # remove 1-letter tokens
            tokens.append(token)

    return tokens


@profile
def parse_quantity(tokens: Sequence[str]) -> Optional[tuple[list[str], set[Quantity]]]:
    """Parses quantities from tokens and deletes quantity tokens."""
    quantities, processed_tokens = set(), []
    units = '|'.join(SI_UNITS + QUANTITY_SPECIAL)

    for token in tokens:
        if (match := regex.fullmatch(f'(\\b\\d+\\.)?\\d+(?P<u>{units})($|\\s)', token)) is not None:
            unit = match.group('u')
            i, quantifier = -len(unit), unit[0] if len(unit) == 2 else ''
            amount = float(token[:i]) if unit in QUANTITY_SPECIAL else float(token[:i]) * QUANTITY_WEIGHTS[quantifier]
            base_unit = unit if unit in QUANTITY_SPECIAL else unit.replace(quantifier, '')
            quantities.add(Quantity(amount, base_unit))
        else:
            processed_tokens.append(token)

    return processed_tokens, quantities if len(processed_tokens) > 0 else None


@profile
def token_equality_check(a: Text, b: Text) -> float:
    """Checks for entirely equal tokens. Very rudimentary."""
    lengths = (len(a.tokens), len(b.tokens))
    matches = len(set(a.tokens) & set(b.tokens))
    length = min(lengths) if min(lengths) >= 4 else max(lengths)  # 'Aura apple juice 0.5L' vs 'Apple'

    if length >= 6:
        return matches / length
    else:  # demand more accuracy for short names (todo: detect brand names? caps lock etc)
        return (matches / length) ** 2


@profile
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


@profile
def find_matches(groups: Sequence[Sequence[Text]]) -> Iterable[SimilarityScore]:
    """Find similar texts between stores (max one element from each set per cluster)."""
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
        sample = '- MINU, rimi coop! 3,5  % 3 * 0,5l kg % plus+ leib- sai a b c '
        result = prepare(sample)
        print(' '.join(result))
        quantity = parse_quantity(result)
        print(quantity)
    # else:
        # groups = prepare_all()
        # find_clusters(groups)
