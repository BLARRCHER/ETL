from db.es_db import ElasticBase
from elasticsearch import helpers
from elasticsearch import TransportError
from el_index import MOVIES_INDEX_BODY as index_body
from typing import Generator
from loguru import logger


class ESLoader(ElasticBase):
    def create_index(self, index: str):
        try:
            self.client.indices.create(index, body=index_body)
        except TransportError as ex:
            logger.warning(ex)

    def generate_elastic_data(self, index_name: str, data: list) -> Generator:
        for item in data:
            movie = {
                '_id': item.id,
                '_index': index_name,
                **item.dict(),
            }
            yield movie

    def save_bulk(self, index: str, data: list) -> None:
        if index == 'movies':
            self.create_index(index)

        res, _ = helpers.bulk(
            self.client,
            self.generate_elastic_data(index, data)
        )
        logger.info(f'Синхронизированно записей {res}')
