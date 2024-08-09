import pytest
import pandas as pd
from eurostatpy.EuroStatPy import EuroStatPy
from eurostatpy.jsonstatpy import JsonStatDataSet

@pytest.fixture
def eurostat_instance():
    return EuroStatPy()

# Test for get_table_from_id
@pytest.mark.asyncio
async def test_get_table_from_id(eurostat_instance):
    result = await eurostat_instance.get_table_from_id("teicp270")
    assert isinstance(result, JsonStatDataSet)
            
# Negative test for get_table_from_id
@pytest.mark.asyncio
async def test_get_table_from_id_invalid_class(eurostat_instance):
    with pytest.raises(Exception) as excinfo:
            await eurostat_instance._EuroStatPy__query_api("table_id")
    assert "API returned with status code:" in str(excinfo.value)

# Test for get_table_from_name
@pytest.mark.asyncio
async def test_get_table_from_name_en(eurostat_instance):
    table_name = eurostat_instance.datasets_en[1]
    result = await eurostat_instance.get_table_from_name(table_name)
    assert isinstance(result, JsonStatDataSet)

@pytest.mark.asyncio
async def test_get_table_from_name_fr(eurostat_instance):
    table_name = eurostat_instance.datasets_fr[3]
    result = await eurostat_instance.get_table_from_name(table_name)
    assert isinstance(result, JsonStatDataSet)

@pytest.mark.asyncio
async def test_get_table_from_name_de(eurostat_instance):
    table_name = eurostat_instance.datasets_de[0]
    result = await eurostat_instance.get_table_from_name(table_name)
    assert isinstance(result, JsonStatDataSet)
                

# Test for get_table_from_id_as_pandas
@pytest.mark.asyncio
async def test_get_table_from_id_as_pandas(eurostat_instance):
    table_id = "ttr00003"
    index = "Time"
    filter = {"geo": "CZ"}
    result = await eurostat_instance.get_table_from_id_as_pandas(table_id, index, filter=filter)
    assert isinstance(result, pd.DataFrame)

# Test for get_table_from_name_as_pandas
@pytest.mark.asyncio
async def test_get_table_from_name_as_pandas_en(eurostat_instance):
    table_name = "Current account - monthly data"
    index = "Time"
    filter = {"geo": "CZ"}
    result = await eurostat_instance.get_table_from_name_as_pandas(table_name, index, filter=filter)
    assert isinstance(result, pd.DataFrame)

@pytest.mark.asyncio
async def test_get_table_from_name_as_pandas_fr(eurostat_instance):
    table_name = "Taux de chômage des jeunes par sexe, âge et région NUTS 2"
    index = "Time"
    filter = {"geo": "FR"}
    result = await eurostat_instance.get_table_from_name_as_pandas(table_name, index, filter=filter)
    assert isinstance(result, pd.DataFrame)

@pytest.mark.asyncio
async def test_get_table_from_name_as_pandas_de(eurostat_instance):
    table_name = "Dienstleistungen - vierteljährliche Daten"
    index = "Time"
    filter = {"geo": "DE"}
    result = await eurostat_instance.get_table_from_name_as_pandas(table_name, index, filter=filter)
    assert isinstance(result, pd.DataFrame)

# Negative test for __query_api
@pytest.mark.asyncio
async def test_query_api_404_error(eurostat_instance):
    table_id = "invalid_table_id"
    with pytest.raises(Exception) as excinfo:
            await eurostat_instance._EuroStatPy__query_api(table_id)
    assert "API returned with status code: 404" in str(excinfo.value)      

def test_datasets_property_en(eurostat_instance):
    assert(isinstance(eurostat_instance.datasets_en, list))
    assert(len(eurostat_instance.datasets_en)>6900)

def test_datasets_property_fr(eurostat_instance):
    assert(isinstance(eurostat_instance.datasets_fr, list))
    assert(len(eurostat_instance.datasets_fr)>6900)

def test_datasets_property_de(eurostat_instance):
    assert(isinstance(eurostat_instance.datasets_de, list))
    assert(len(eurostat_instance.datasets_de)>6900)

def test_codes_property(eurostat_instance):
    assert(isinstance(eurostat_instance.codes, set))
    assert(len(eurostat_instance.codes)>6900)

def test_list_datasets_en(eurostat_instance, capsys):
    eurostat_instance.list_datasets()
    captured = capsys.readouterr()
    assert len(captured.out) > 6000

def test_list_datasets_fr(eurostat_instance, capsys):
    eurostat_instance.list_datasets(language="fr")
    captured = capsys.readouterr()
    assert len(captured.out) > 6000

def test_list_datasets_de(eurostat_instance, capsys):
    eurostat_instance.list_datasets(language="de")
    captured = capsys.readouterr()
    assert len(captured.out) > 6000