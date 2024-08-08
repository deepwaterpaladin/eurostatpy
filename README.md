# EuroStatPy

[![Upload Python Package](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/publish.yml/badge.svg)](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/publish.yml)

Basic package for querying &amp; downloading EuroStat data by dataset name or ID. Currently saves data into `JSONStat` [format](https://github.com/26fe/jsonstat.py).

Allows for querying datasets via plain text search or table ID.

## Installation

`pip install eurostatpy`

## Usage

### Download Data by Name

```python
from eurostatpy.EuroStatPy import EuroStatPy
euroStat = EuroStatPy()
euroStat.get_table_from_name("Energy taxes by paying sector")
```

### Download Data by Table ID

```python
euroStat.get_table_from_id("rail_tf_ns20_hu")
```

### List Avaiable Table Names

```python
euroStat.datasets
>>> ['Population connected to wastewater treatment plants', ...]
```

### List Avaiable Table IDs

```python
euroStat.codes
>>> ['env_waspb', ...]
```

## TODO

1. Write test(s)
1. Add pandas support
1. Add pyspark support

## Further Reading

- [EuroStat Data](https://ec.europa.eu/eurostat/web/main/data/database)
- [EuroStat API](https://wikis.ec.europa.eu/display/EUROSTATHELP/API+-+Getting+started+with+statistics+API)
