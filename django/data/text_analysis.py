"""Product title text analysis."""

from typing import Iterable, NamedTuple, Sequence
import itertools as it

from unidecode import unidecode
import regex


BLACKLIST = ('ja', 'hulgi', 'rimi', 'coop', 'selver', 'selveri pagarid', 'selveri köök', 'coop kokad')
WHITELIST = ()

QTY_UNITS = ('g', 'l', 'm')
QTY_WEIGHTS = {'m': 1 / 1000, 'c': 1 / 100, 'd': 1 / 10, 'k': 1000, '': 1}  # '' must be last for regex!
SI_UNITS = tuple(f'{w}{q}' for w, q in it.product(QTY_WEIGHTS.keys(), QTY_UNITS))
SPECIAL_UNITS = ('%', 'tk', 'gr')  # gr->g alias, rl, kmpl
UNITS = SI_UNITS + SPECIAL_UNITS


Quantity = NamedTuple('Quantity', amount=float, unit=str)
Text = NamedTuple('Text', id=int, barcode=str, tokens=Sequence[str], quantity=set[Quantity])  # original=str


def prepare_store(store: dict) -> list[Text]:
    """Prepare all products of a store."""
    results: list[Text] = []
    for product in store:
        tokens = prepare(product['name'])
        if len(tokens) == 0:
            continue
        tokens, quantities = parse_quantity(tokens)

        barcode = product['hash'] if product['has_barcode'] else ''
        text_record = Text(product['id'], barcode, tokens, quantities)
        results.append(text_record)
    return results


def prepare(text: str) -> list[str]:
    """Prepare text through tokenization, transformation, normalization, and filtering."""
    text = regex.sub(r'\u00B4|\u24C7|`|"|\'|\+', '', text.lower())
    text = regex.sub(r'\u00D7|\+|&|\(|\)', ' ', text)
    text = regex.sub(r',\s*(\D)', r' \1', text)

    text = unidecode(text)  # remove diacritics

    # todo: hyphenated words, e.g. 'singi-juustupirukas'; do we separate, add, keep, multiple?
    text = regex.sub(r'(\d+\s*),(\s*\d+)', r'\1.\2', text)  # normalize commas
    text = regex.sub(r'(\d+)\s*(?:\*|x)\s*(\d+)(?=\s*+\D)', r'\1x\2', text)  # 3 * 5 kg -> 3x5 kg
    text = text.replace('%vol', '% vol')  # 3.5%vol -> 3.5% vol
    text = text.replace('/', ' ')
    text = text.replace('e-piim', '$$EPIIM$$')
    text = text.replace('-', ' ')
    text = text.replace('$$EPIIM$$', 'e-piim')

    # tokenize the string
    tokens = []
    for token in text.split():
        token = regex.sub(r'(?:-|,|!|\.)$', '', token)  # remove junk characters
        token = token.strip()

        if token in BLACKLIST:
            continue

        if token in UNITS:
            if len(tokens) > 0 and tokens[-1].replace('.', '').isdigit():
                tokens[-1] = tokens[-1] + token  # 3 tk -> 3tk
                continue
            elif token not in SPECIAL_UNITS or token == 'gr':
                token = '1' + token  # kg -> 1kg

        if len(token) >= 2 or token.isdigit():  # remove 1-letter tokens
            tokens.append(token)

    return tokens


def parse_quantity(tokens: Sequence[str], *, force_extraction=False) -> tuple[Sequence[str], set[Quantity]]:
    """Parse quantities from tokens and delete quantity tokens."""
    quantities, processed_tokens = set(), []
    units = '|'.join(SI_UNITS + SPECIAL_UNITS)

    for token in tokens:
        pattern = f'(\\d+x)?((?<=x|\\b)\\d+\\.)?\\d+(?P<u>{units})($|\\s)'
        if (match := regex.fullmatch(pattern, token)) is not None:
            unit = match.group('u')
            i, quantifier = -len(unit), unit[0] if len(unit) == 2 else ''
            if unit == 'gr':  # alias
                quantifier, unit = '', 'g'

            num = token[:i]
            if 'x' in num:  # e.g. '3x5tk'
                multiplier, multiplicand = int(num.split('x')[0]), float(num.split('x')[1])
                if unit == '%':  # something like '3x5%' makes no sense
                    multiplier = 1
                amount = multiplier * multiplicand
            else:
                amount = float(num)

            if unit not in SPECIAL_UNITS:
                amount *= QTY_WEIGHTS[quantifier]

            base_unit = unit if unit in SPECIAL_UNITS else unit.replace(quantifier, '', 1)
            quantities.add(Quantity(amount, base_unit))
        else:
            processed_tokens.append(token)

    if force_extraction:  # Extract quantities even if it results in no remaining tokens
        return processed_tokens, quantities
    return (processed_tokens, quantities) if len(processed_tokens) > 0 else (tokens, set())


def token_equality_check(a: Text, b: Text) -> float:
    """Check for entirely equal tokens."""
    lengths = (len(a.tokens), len(b.tokens))
    matches = len(set(a.tokens) & set(b.tokens))
    length = min(lengths) if min(lengths) >= 4 else max(lengths)  # 'Aura apple juice 0.5L' vs 'Apple'

    if length >= 6:
        return matches / length
    else:  # demand more accuracy for short names (todo: detect brand names? caps lock etc)
        return (matches / length) ** 2


def similarity_check(a: Text, b: Text) -> float:
    """Perform similary checks on two token sequences (combining multiple similarity check algorithms)."""
    if a.quantity != b.quantity:
        return 0
    return token_equality_check(a, b)


SimilarityScore = NamedTuple('SimilarityScore', score=float, id_a=int, id_b=int)


def find_matches(groups: Sequence[Sequence[Text]]) -> Iterable[SimilarityScore]:
    """Find similar texts between stores (max one element from each set per cluster)."""
    results: list[SimilarityScore] = []
    combinations = list(it.combinations(groups, 2))
    for i, (a_group, b_group) in enumerate(combinations):
        print(f'Processing new store combination... ({i + 1}/{len(combinations)})')
        for a in a_group:  # it.product()
            highest = 0.8  # lower bound is 0.8, else score is ignored entirely at start
            highest_b_id = None  # ID of highest match so far
            valid_match = False  # no match at first if the lower bound isn't surpassed

            for b in b_group:
                if (score := similarity_check(a, b)) >= 0.8:
                    if score > highest:
                        # highest, valid_match = SimilarityScore(round(score, 2), a.id, b.id), False
                        highest, highest_b_id, valid_match = score, b.id, True
                    elif score == highest:  # multiple equal strength matches -> there is no quality match
                        valid_match = False

            if valid_match:
                results.append(SimilarityScore(round(highest, 2), a.id, highest_b_id))

    print('Storing results...')
    yield from results
