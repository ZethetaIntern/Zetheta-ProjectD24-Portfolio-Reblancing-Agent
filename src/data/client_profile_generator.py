# Client overlays used to make portfolios more realistic.

import numpy as np

def generate_client_profile(portfolio_id, seed=42):
    # Synthetic client metadata; no real personal data is stored.
    rng = np.random.default_rng(seed + hash(portfolio_id) % 10000)
    return {
        "portfolio_id": portfolio_id,
        "ethical_exclusions": [],
        "sector_preferences": {},
        "single_stock_restrictions": [],
        "liquidity_need": float(rng.uniform(0, .20)),
        "tax_bracket": float(rng.choice([.10, .20, .30])),
    }
