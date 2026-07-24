# Dataset Selection Report

## Decision

Use state-wise Indian crime data from 2001-2023 for the MVP. This is cleaner than district-wise data, easier to merge with demographic features, and still demonstrates forecasting, explainability, and geospatial visualization.

## Selected Sources

| Dataset | Source URL | Features | Years | Join Key | Missing Values / Issues | Suitable |
|---|---|---|---|---|---|---|
| NCRB Crime in India state-wise crime data | https://www.data.gov.in/catalog/crime-india-2023 and annual NCRB Crime in India catalogs | State/UT, year, IPC/BNS crimes, SLL crimes, crime heads, rates depending on table | 2001-2023 | State/UT, Year | Older resources may have no API; names and state reorganizations need normalization | Yes |
| Census of India Primary Census Abstract | https://censusindia.gov.in/census.website/data/population-finder | Population, households, rural/urban split, worker categories | 2001, 2011 | State/UT | Decadal only; interpolate or combine with projections | Yes |
| Population Projections for India and States 2011-2036 | https://www.mohfw.gov.in/?q=reports-0 | Annual projected population by state | 2011-2036 | State/UT, Year | Projections, not observed census values | Yes |
| Census literacy rates | https://www.data.gov.in/resource/stateuts-wise-literacy-rates-census-2001-and-2011 | Literacy rate | 2001, 2011 | State/UT | Decadal only | Yes, optional |
| Urban population percentage | https://www.data.gov.in/resource/stateut-wise-percentage-urban-population-total-population-and-decennial-growth-rate | Urban population %, decennial growth | 1991-2001, 2001-2011 | State/UT | Not annual | Yes, optional |
| UDISE+ | https://udiseplus.gov.in/ | Education and school indicators | Mostly 2019 onward in accessible public tables | State/UT, academic year | Insufficient 2001-2023 coverage | No for MVP |
| NITI Aayog SDG India Index | https://www.niti.gov.in/reports-sdg | SDG composite and goal-wise scores | 2018, 2019, 2020-21, 2023-24 | State/UT, report year | Sparse, index-based | No for MVP model |

## Processed CSV Schema

```csv
state,year,crime_count,population,literacy_rate,urban_population_pct,latitude,longitude
```

## Replacement Plan

1. Download official NCRB annual CSV/ZIP/PDF tables into `data/raw/ncrb/`.
2. Normalize state names and year fields.
3. Join Census and MoHFW features on `state + year`.
4. Write the final clean file to `data/processed/state_crime_2001_2023.csv`.
5. Re-run `python ml/train_models.py`.

