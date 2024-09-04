from .jsonstatpy import JsonStatDataSet
from .utilities import read_xml_to_dict
import pandas as pd
import aiohttp
import os


class EuroStatPy:
    """
    Class to interact with the EuroStat API and retrieve datasets in various formats.

    Attributes:
    - base (str): The base URL for the Eurostat API.
    - tail (str): The URL tail used to specify the format and language of the returned data.
    - since_time_period (str): A query parameter to filter data since a specific time period. For performance reasons, most datasets are only available from 2020 to present (resolution coming v.1.1.0).
    """
    def __init__(self) -> None:
        """
        Initializes the EuroStatPy object.
        """
        self.base = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
        self.tail = "?format=JSON&lang=EN"
        self.since_time_period = "&sinceTimePeriod=2020"

    @property
    def datasets_en(self) -> list[str]:
        """
        Retrieves a list of English dataset IDs available in the local Eurostat schema.

        Returns:
        - list[str]: A list of dataset IDs.
        """
        raw_datasets = self.__get_datasets(language="en").items()
        return [i[0] for i in raw_datasets]
    
    @property
    def datasets_fr(self) -> list[str]:
        """
        Retrieves a list of French dataset IDs available in the local Eurostat schema.

        Returns:
        - list[str]: A list of dataset IDs.
        """
        raw_datasets = self.__get_datasets(language="fr").items()
        return [i[0] for i in raw_datasets]
    
    @property
    def datasets_de(self) -> list[str]:
        """
        Retrieves a list of German dataset names available in the local Eurostat schema.

        Returns:
        - list[str]: A list of dataset IDs.
        """
        raw_datasets = self.__get_datasets(language="de").items()
        return [i[0] for i in raw_datasets]

    @property
    def codes(self) -> set[str]:
        """
        Retrieves a list of dataset codes available in the local Eurostat schema.

        Returns:
        - list[str]: A list of dataset codes.
        """
        raw_datasets = self.__get_datasets().items()
        return set([i[1] for i in raw_datasets])
    
    async def get_table_from_id(self, table_id: str) -> JsonStatDataSet:
        """
        Retrieves a dataset from the Eurostat API using the dataset's ID.

        Args:
        - table_id (str): The ID of the dataset to retrieve.

        Returns:
        - JsonStatDataSet: A JsonStatDataSet object containing the dataset.
        """
        data = await self.__query_api(table_id)
        if data['class'] == 'dataset':
            jsonStatDataSet = JsonStatDataSet()
            jsonStatDataSet._from_json_v2(data)
            return jsonStatDataSet
        else:
            raise Exception(f"API returned type {data['class']} which isn't currently supported by the package.")

    async def get_table_from_name(self, table_name: str) -> JsonStatDataSet:
        """
        Retrieves a dataset from the Eurostat API using the dataset's name.

        Args:
        - table_name (str): The name of the dataset to retrieve.

        Returns:
        - JsonStatDataSet: A JsonStatDataSet object containing the dataset.
        """
        id = self.__get_id_from_name(table_name)
        data = await self.__query_api(id)
        if data['class'] == 'dataset':
            jsonStatDataSet = JsonStatDataSet()
            jsonStatDataSet._from_json_v2(data)
            return jsonStatDataSet
        else:
            raise Exception(f"API returned type {data['class']} which isn't currently supported by the package.")
    
    async def get_table_from_id_as_pandas(self, table_id: str, index:str, filter:dict[str,str]=None, content:str="label") -> pd.DataFrame:
        """
        Retrieves a dataset from the Eurostat API using the dataset's ID and converts it to a pandas DataFrame.

        Args:
        - table_id (str): The ID of the dataset to retrieve.
        - index (str): The column to set as the index in the resulting DataFrame.
        - filter (dict[str, str], optional): A dictionary to filter the dataset by specific dimensions. Defaults to None.
        - content (str, optional): The content type of the dataset's values ('label', 'id', etc.). Defaults to 'label'.

        Returns:
        - pd.DataFrame: The dataset as a pandas DataFrame.
        """
        jsd = await self.get_table_from_id(table_id)
        return jsd.to_data_frame(index, content=content, blocked_dims=filter)

    async def get_table_from_name_as_pandas(self, table_name: str, index:str, filter:dict[str,str]={}, content:str="label") -> pd.DataFrame:
        """
        Retrieves a dataset from the Eurostat API using the dataset's name and converts it to a pandas DataFrame.

        Args:
        - table_name (str): The name of the dataset to retrieve.
        - index (str): The column to set as the index in the resulting DataFrame.
        - filter (dict[str, str], optional): A dictionary to filter the dataset by specific dimensions. Defaults to an empty dictionary.
        - content (str, optional): The content type of the dataset's values ('label', 'id', etc.). Defaults to 'label'.

        Returns:
        - pd.DataFrame: The dataset as a pandas DataFrame.
        """
        jsd = await self.get_table_from_name(table_name)
        return jsd.to_data_frame(index, content=content, blocked_dims=filter)


    def list_datasets(self, language:str="en") -> None:
        """
        Prints a list of available datasets with their corresponding codes from the local Eurostat schema.
        """
        datasets = self.__get_datasets(language).items()
        idx = 1
        for ds in datasets:
            print(f"{idx}. Dataset: {ds[0]} | Code: {ds[1]}")
            idx += 1

    async def __query_api(self, table_id: str, retry_url: str = None) -> dict:
        """
        Queries the Eurostat API for a dataset based on the dataset's ID.

        Args:
        - table_id (str): The ID of the dataset to retrieve.
        - retry_url (str, optional): A URL to retry the query if the initial query fails. Defaults to None.

        Returns:
        - dict: The JSON response from the API.

        Raises:
        - Exception: If the API returns a status code other than 200 or 413.
        """

        url = f"{self.base}{table_id}{self.tail}" if retry_url is None else retry_url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 413:
                    await self.__query_api(table_id=table_id, retry_url=f"{self.base}{table_id}{self.tail}&sinceTimePeriod=2024")
                else:
                    raise Exception(
                        f"API returned with status code: {response.status}\n{await response.text()}")

    def __get_datasets(self, language:str=None) -> dict: # type: ignore
        """
        Loads and flattens the Eurostat dataset schema from a local JSON file.

        Returns:
        - list[tuple[str, str]]: A list of tuples containing the dataset path and code.
        """
        path = os.path.join(os.path.dirname(__file__),"schema", "table_of_contents.xml")
        return read_xml_to_dict(path, language)

    def __get_id_from_name(self, table_name: str) -> str:
        """
        Retrieves the dataset ID based on the dataset's name.

        Args:
        - table_name (str): The name of the dataset.

        Returns:
        - str: The ID of the dataset.

        Raises:
        - Exception: If the dataset name is not found in the local schema.
        """
        try:
            datasets = self.__get_datasets()
            # TODO: Fix this
            for k, v in datasets.items():
                if table_name in k:
                    return v
            raise Exception(f"Table name: {table_name} not found in dataset.")
        except Exception as e:
            raise e
