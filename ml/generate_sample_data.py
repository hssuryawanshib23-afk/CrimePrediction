"""Generate a local 2001-2023 state-wise dataset for development.

The CSV schema mirrors the official-data target:
state, year, crime_count, population, literacy_rate, urban_population_pct.
Replace this generated file with cleaned NCRB/Census data when available.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "state_crime_2001_2023.csv"

STATES = [
    ("Andhra Pradesh", 15.9129, 79.74, 95000, 76210000, 67.0, 27.3),
    ("Arunachal Pradesh", 28.2180, 94.7278, 2800, 1100000, 54.3, 20.8),
    ("Assam", 26.2006, 92.9376, 68000, 26660000, 63.3, 12.9),
    ("Bihar", 25.0961, 85.3131, 105000, 82999000, 47.0, 10.5),
    ("Chhattisgarh", 21.2787, 81.8661, 52000, 20830000, 64.7, 20.1),
    ("Delhi", 28.7041, 77.1025, 78000, 13850000, 81.7, 93.0),
    ("Goa", 15.2993, 74.1240, 4200, 1350000, 82.0, 49.8),
    ("Gujarat", 22.2587, 71.1924, 118000, 50670000, 69.1, 37.4),
    ("Haryana", 29.0588, 76.0856, 72000, 21140000, 67.9, 28.9),
    ("Himachal Pradesh", 31.1048, 77.1734, 15000, 6078000, 76.5, 9.8),
    ("Jharkhand", 23.6102, 85.2799, 41000, 26940000, 53.6, 22.2),
    ("Karnataka", 15.3173, 75.7139, 124000, 52850000, 66.6, 34.0),
    ("Kerala", 10.8505, 76.2711, 82000, 31840000, 90.9, 26.0),
    ("Madhya Pradesh", 22.9734, 78.6569, 165000, 60380000, 63.7, 26.5),
    ("Maharashtra", 19.7515, 75.7139, 195000, 96880000, 76.9, 42.4),
    ("Manipur", 24.6637, 93.9063, 5200, 2294000, 70.5, 23.9),
    ("Meghalaya", 25.4670, 91.3662, 4600, 2319000, 62.6, 19.6),
    ("Mizoram", 23.1645, 92.9376, 2600, 889000, 88.8, 49.6),
    ("Nagaland", 26.1584, 94.5624, 2200, 1990000, 66.6, 17.2),
    ("Odisha", 20.9517, 85.0985, 64000, 36700000, 63.1, 15.0),
    ("Punjab", 31.1471, 75.3412, 41000, 24360000, 69.7, 34.0),
    ("Rajasthan", 27.0238, 74.2179, 108000, 56510000, 60.4, 23.4),
    ("Sikkim", 27.5330, 88.5122, 1000, 541000, 68.8, 11.1),
    ("Tamil Nadu", 11.1271, 78.6569, 150000, 62110000, 73.5, 44.0),
    ("Telangana", 18.1124, 79.0193, 62000, 30500000, 66.5, 38.7),
    ("Tripura", 23.9408, 91.9882, 4200, 3199000, 73.2, 17.0),
    ("Uttar Pradesh", 26.8467, 80.9462, 235000, 166200000, 56.3, 20.8),
    ("Uttarakhand", 30.0668, 79.0193, 16000, 8489000, 71.6, 25.6),
    ("West Bengal", 22.9868, 87.8550, 142000, 80220000, 68.6, 28.0),
]


def main() -> None:
    """Generate deterministic state-year data."""

    rng = np.random.default_rng(seed=42)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = []

    for index, (state, lat, lon, base_crime, base_pop, literacy_2001, urban_2001) in enumerate(STATES):
        annual_growth = 0.012 + (index % 6) * 0.002
        crime_level = float(base_crime)
        for year in range(2001, 2024):
            t = year - 2001
            population = base_pop * ((1 + annual_growth) ** t)
            literacy = min(literacy_2001 + t * (0.45 + (index % 5) * 0.03), 96.0)
            urban = min(urban_2001 + t * (0.18 + (index % 4) * 0.06), 98.0)
            seasonal = 1 + 0.04 * np.sin((t + index) / 2.7)
            policy_noise = rng.normal(0, 0.035)
            crime_level = max(crime_level * (1 + 0.015 + policy_noise), base_crime * 0.7)
            crime_count = crime_level * seasonal + (population / 1_000_000) * 35

            rows.append(
                {
                    "state": state,
                    "year": year,
                    "crime_count": int(round(crime_count)),
                    "population": int(round(population)),
                    "literacy_rate": round(literacy, 2),
                    "urban_population_pct": round(urban, 2),
                    "latitude": lat,
                    "longitude": lon,
                }
            )

    with OUTPUT_PATH.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

