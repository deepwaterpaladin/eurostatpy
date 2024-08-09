# EuroStatPy

[![Upload Python Package](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/publish.yml/badge.svg)](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/publish.yml)

[![Unit Tests](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/qa-tests.yml/badge.svg)](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/qa-tests.yml)

Basic package for querying &amp; downloading EuroStat data by dataset name or ID. Currently saves data into `JSONStat` [format](https://github.com/26fe/jsonstat.py) or a `pandas.DataFrame`.

Allows for querying datasets via plain text search or table ID.

## Installation

`pip install eurostatpy`

## Usage

### Importing

```python
from eurostatpy import EuroStatPy
euroStat = EuroStatPy()
```

### Download Data by Name

```python
euroStat.get_table_from_name("Energy taxes by paying sector")
>>> `JSONStat` object

euroStat.get_table_from_name_as_pandas("Energy taxes by paying sector")
>>> `pandas.DataFrame` object
```

### Download Data by ID

```python
euroStat.get_table_from_id("rail_tf_ns20_hu")
>>> `JSONStat` object

euroStat.get_table_from_id_as_pandas("rail_tf_ns20_hu")
>>> `pandas.DataFrame` object
```

### List Available Table Names in English, French, and German

```python
euroStat.datasets_en
>>> ["Population connected to wastewater treatment plants", ...]
euroStat.datasets_fr
>>> ["Compte courant - données trimestrielles", ...]
euroStat.datasets_de
>>> ["Leistungsbilanz - vierteljährliche Daten", ...]
```

### List Available Table IDs

```python
euroStat.codes
>>> ["env_waspb", "rail_tf_ns20_hu", ...]
```

### Print Available Datasets in English, French, and German

```python
euroStat.list_datasets()
>>> "1. Dataset: Current account - quarterly data | Code: ei_bpm6ca_q
     2. Dataset: Financial account - quarterly data | Code: tipsbp48
     ...
     6930. Dataset: Youth unemployment ratio by sex, age and NUTS 2 regions | Code: yth_empl_140"
euroStat.list_datasets(language = "fr")
>>> "1. Compte courant - données trimestrielles | Code: ei_bpm6ca_q
     2. Dataset: Compte financier - données trimestrielles | Code: tipsbp48
     ...
     6920. Dataset: Ratio de chômage des jeunes par sexe, âge et région NUTS 2 | Code: yth_empl_140"
euroStat.list_datasets(language = "de")
>>> "1. Dataset: Leistungsbilanz - vierteljährliche Daten | Code: tipsbp40
     2. Dataset: Finanzierungskonto - vierteljährliche Daten | Code: tipsbp48
     ...
     6922. Dataset: Anteil der arbeitslosen Jugendlichen nach Geschlecht, Alter und NUTS-2-Regionen | Code: yth_empl_140"
```

## Further Reading

- [EuroStat Data](https://ec.europa.eu/eurostat/web/main/data/database)
- [EuroStat API](https://wikis.ec.europa.eu/display/EUROSTATHELP/API+-+Getting+started+with+statistics+API)
