# Maison aux Tulipes - factual review packet

Date: 2026-09-16
Article id: `maison-aux-tulipes-bratislava-jeno-schiller`
Status: ready for final editorial review, not approved for publication

## Review purpose

This packet resolves the pending date and separates the official heritage record
from a plausible but not yet institutionally verified architect attribution. It also
documents why `Maison aux Tulipes` remains an editorial title rather than the exact
official name.

## Controlling source

The Pamiatkový úrad Slovenskej republiky publishes its heritage registers as daily
open-data exports under CC BY 4.0:

- [Open-data portal](https://www.pamiatky.sk/online-sluzby/open-data)
- [Immovable national cultural monuments XML](https://www.pamiatky.sk/fileadmin/documents/opendata/nehnutelne-narodne-kulturne-pamiatky.xml)
- [Heritage objects XML](https://www.pamiatky.sk/fileadmin/documents/opendata/pamiatkove-objekty.xml)

The relevant records are national monument `NNKP508`, ÚZPF `637`, and heritage
object `PO883`, ÚZPF `637/1`. The portal warns that the data are informative rather
than legal extracts, but they are the authoritative public register for editorial
fact checking.

## Confirmed facts

| Field | Confirmed value | Public article state |
|---|---|---|
| Registered usual name | `Tulipán, hotel Roset` | Stored as `identity.exact_name` |
| Editorial title | `Maison aux Tulipes` | Retained as a readable French title, not claimed as the exact registered name |
| Building type | Corner residential building | Compatible with `identity.type: building` |
| Address | Štúrova 10, Bratislava-Staré Mesto | Normalized in stable facts and all locale blocks |
| Construction year | 1903 | Added to stable facts and all locale blocks |
| Dominant style | `secesia` | Rendered as Art nouveau / Sécession according to locale |
| Protection | National cultural monument, ÚZPF 637 | Recorded internally, not added to the public copy |

## Architect attribution

The official heritage open-data records do not name an architect. The building's
current operator states that it was designed in 1903 by Jenő Schiller:

- [Roset Hotel, The House](https://rosethotel.sk/hotel)

The spelling `Jenő Schiller` is also consistent with Peter Buday's academic work on
the Bratislava architect, listed by Comenius University. The university record does
not expose a building-by-building attribution, so it cannot by itself close this
claim:

- [Comenius University, Peter Buday profile and publications](https://ais2.uniba.sk/repo2/repository/default/ais/zamestnanec/FiF/SK/buday4.uniba.sk.html)

The article therefore keeps Schiller only as an attribution. His name was removed
from the stable `facts.people` block, which is reserved for confirmed facts, and is
displayed as `attributed` in the three practical-information blocks.

## Name and motif caution

`Maison aux Tulipes` is a useful editorial translation of the established
`Tulipán` name, but it must not be used as proof that every visible floral or curved
form represents a tulip. The support photograph was described neutrally as a glazed
entrance with curved lines and repeated teardrop-shaped motifs. No flower species,
architect or building identity is inferred from the photograph alone.

## Claims not approved from this packet

Do not publish as established facts without a stronger directly consulted source:

- Samuel and Anna Fischer as commissioners;
- Jenő Schiller's age when the building was designed;
- the original number of storeys;
- a precise `Viennese Secession` classification;
- the detailed sequence or dates of restoration;
- a claim that the visible motifs are specifically tulips.

## Accessibility review

An independent image review confirmed the order and fidelity of the FR, EN and NL
support-image alternatives. The descriptions deliberately avoid historical or
iconographic interpretation. The regression test now checks every runtime article
that contains a support image, rather than maintaining a manual list of completed
articles.

## Remaining human gate

Before a separate publication-status pull request, the reviewer must:

1. approve the cautious `attributed to Jenő Schiller` wording in FR, EN and NL;
2. approve `Maison aux Tulipes` as the editorial title alongside the registered name;
3. read all three language versions for tone and equivalence;
4. confirm the image order and crops on the deployed preview;
5. choose the real publication date;
6. explicitly approve the move from `draft` to `published`.
