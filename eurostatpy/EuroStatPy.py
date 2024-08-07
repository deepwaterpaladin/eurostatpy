from .jsonstatpy import JsonStatDataSet
import pandas as pd
import json
import aiohttp
import os


class EuroStatPy:
    def __init__(self, path: str = None) -> None:
        self.path = "./temp" if path is None else path
        self.base = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
        self.tail = "?format=JSON&lang=EN"
        self.since_time_period = "&sinceTimePeriod=2020"

    async def get_table_from_id(self, table_id: str) -> JsonStatDataSet:
        data = await self.__query_api(table_id)
        if data['class'] == 'dataset':
            jsonStatDataSet = JsonStatDataSet()
            jsonStatDataSet._from_json_v2(data)
            return jsonStatDataSet
        else:
            return f"API returned type {data['class']} which isn't currently supported by the package."

    async def get_table_from_name(self, table_name: str) -> JsonStatDataSet:
        id = self.__get_id_from_name(table_name)
        data = await self.__query_api(id)
        if data['class'] == 'dataset':
            jsonStatDataSet = JsonStatDataSet()
            jsonStatDataSet._from_json_v2(data)
            return jsonStatDataSet
        else:
            return f"API returned type {data['class']} which isn't currently supported by the package."

    def get_table_from_id_as_pandas(self, table_id: str) -> pd.DataFrame:
        jsd = self.get_table_from_id(table_id)
        return jsd.to_data_frame()

    def get_table_from_name_as_pandas(self, table_name: str) -> pd.DataFrame:
        jsd = self.get_table_from_name(table_name)
        return jsd.to_data_frame()

    @property
    def datasets(self) -> list[str]:
        raw_datasets = self.__get_datasets()
        return list(set(i[0].split('/')[-1] for i in raw_datasets))

    @property
    def codes(self) -> list[str]:
        raw_datasets = self.__get_datasets()
        return list(set(i[-1] for i in raw_datasets))

    def list_datasets(self) -> None:
        datasets = self.__get_datasets()
        idx = 1
        for ds in datasets:
            spds = ds[0].split('/')
            print(f"{idx}. Dataset: {spds[-1]} | Code: {ds[1]}")
            idx += 1

    async def __query_api(self, table_id: str, retry_url: str = None) -> dict:
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

    def __flatten_json(self, json_obj, parent_key='') -> list[tuple]:
        """
        Recursively flattens a nested JSON object into a list of tuples.

        Args:
        - json_obj (dict or list): The JSON object to flatten.
        - parent_key (str): The base key string to prefix the keys in the tuples.

        Returns:
        - List[Tuple[str, str]]: A list of tuples where each tuple is (key, value).
        """
        items = []
        if isinstance(json_obj, dict):
            for k, v in json_obj.items():
                new_key = f"{parent_key}/{k}" if parent_key else k
                if isinstance(v, dict) or isinstance(v, list):
                    items.extend(self.__flatten_json(v, new_key))
                else:
                    items.append((new_key, v))
        elif isinstance(json_obj, list):
            for i, item in enumerate(json_obj):
                new_key = f"{parent_key}/{i}" if parent_key else str(i)
                items.extend(self.__flatten_json(item, new_key))

        return items

    def __get_datasets(self):
        path = os.path.join("schema", "eu_database.json")
        with open(path, 'r') as file:
            data = json.load(file)
        return self.__flatten_json(data)

    def __get_id_from_name(self, table_name: str) -> str:
        try:
            datasets = self.__get_datasets()
            # TODO: Fix this
            for k, v in datasets:
                if table_name in k:
                    return v
            raise Exception(f"Table name: {table_name} not found in dataset.")
        except Exception as e:
            raise e
