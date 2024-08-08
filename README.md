# EuroStatPy

[![Upload Python Package](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/publish.yml/badge.svg)](https://github.com/deepwaterpaladin/eurostatpy/actions/workflows/publish.yml)

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

## TODO

1. Write test(s)
1. Add pyspark support

## Further Reading

- [EuroStat Data](https://ec.europa.eu/eurostat/web/main/data/database)
- [EuroStat API](https://wikis.ec.europa.eu/display/EUROSTATHELP/API+-+Getting+started+with+statistics+API)
