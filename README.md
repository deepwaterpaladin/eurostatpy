# EuroStatPy

[![Upload Python Package](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/publish.yml/badge.svg)](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/publish.yml)

[![Unit Tests](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/qa-tests.yml/badge.svg)](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/qa-tests.yml)

Basic package for querying &amp; downloading EuroStat data by dataset name or ID. Currently saves data into `JSONStat` [format](https://github.com/26fe/jsonstat.py).

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

### List Avaiable Table Names

```python
euroStat.datasets
>>> ["Population connected to wastewater treatment plants", ...]
```

### List Avaiable Table IDs

```python
euroStat.codes
>>> ["env_waspb", "rail_tf_ns20_hu", ...]
```

### Print Avaiable Datasets

```python
euroStat.list_datasets()
>>> "1. Dataset: Commercial airports by type | Code: avia_if_arp
     2. Dataset: Airport infrastructures by type | Code: avia_if_typ
     3. Dataset: Airport connections to transport infrastructure | Code: avia_if_arp_co
     ...
     513. Dataset: Cooling and heating degree days by NUTS 3 regions - monthly data | Code: nrg_chddr2_m"
```

## Further Reading

- [EuroStat Data](https://ec.europa.eu/eurostat/web/main/data/database)
- [EuroStat API](https://wikis.ec.europa.eu/display/EUROSTATHELP/API+-+Getting+started+with+statistics+API)
