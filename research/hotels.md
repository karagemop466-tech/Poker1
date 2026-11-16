# T3: Hotel research log

Session `1fafb3d2` · Checked 2026-11-16 · Output: `data/hotels.json` (7 hotels), built by `scripts/build_data.py`.

## Scope
Hotels within walking range of the Venetian poker room (host property) and Wynn Las Vegas. The list is limited to hotels whose official pages were reachable in this session.

## Verified
| Item | Hotel | Source (official) | Status |
|---|---|---|---|
| Resort fee $55 plus tax per night | The Venetian | [resort fee page](https://www.venetianlasvegas.com/resort/resort-fee.html) (search excerpt) | verified (excerpt) |
| Resort fee $55 per night | The Palazzo | [poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html) | verified; tax not stated |
| Resort fee $55 plus tax per night | Wynn Las Vegas, Encore | [Wynn terms](https://www.wynnlasvegas.com/terms-and-conditions/848671) (search excerpt) | verified (excerpt) |
| Clark County room tax 13.38% | all | [Venetian hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) (search excerpt) | verified (excerpt); applies to fee: unconfirmed |
| Venetian poker-suite rates "as low as $119 and $209" | Venetian, Palazzo | [poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html) | conditional; not assigned to a property |

## Not verified (left blank)
- Room rate per night for every hotel on every date.
- Resort fee for Bellagio (no official MGM page found), Caesars Palace (official range $45 to $50 only), ARIA (official home page read; no fee terms found).
- Walking time from any hotel to any venue.

## Method
- True cost per night = (room rate + resort fee) × 1.1338. This formula assumes the room tax applies to the resort fee. It is not verified, and the value stays blank until a room rate is verified.
