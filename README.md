# Blackjack · The Arcade

Jason Breedlove’s Python Blackjack, with a responsive emerald-and-gold browser table. The browser runs **Python**, using Pyodide; JavaScript renders cards and handles input. The original Pygame files and image assets remain intact.

## Play
Deal, Hit, or Stand. Aces adjust between 1 and 11, face cards count as 10, and the dealer stands on all 17s. Two-card naturals settle immediately; other 21s resolve the dealer turn. Equal totals push. One freshly shuffled 52-card deck per hand, no betting, splitting, doubling, or insurance. Session scores reset on reload. The first visit downloads the Python runtime.

## Development
- `npm test` — Python rule tests (Python 3 required).
- `npm run build` — dependency-free static build in `dist`.
- `python3 -m http.server 8000 -d dist` — serve locally after building.
- Vercel: Other framework, build `npm run build`, output `dist`. No secrets or database required.

`engine.py` adapts the original Deck / Hand logic into an import-safe rules module. It fixes multi-ace totals, removes the five-card limit, and prevents actions after settlement. `blackjack.py` and `blackjack_pygame.py` preserve the earlier desktop implementations; they require Pygame and retain their original behavior. New card faces are rendered in HTML/CSS without external card artwork.
