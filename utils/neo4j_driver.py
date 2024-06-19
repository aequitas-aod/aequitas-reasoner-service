from time import sleep
from typing import List

from neo4j import GraphDatabase, Driver, Result
from neo4j.exceptions import ServiceUnavailable


class Credentials:
    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password


class Neo4jQuery:
    def __init__(self, query: str, params: dict):
        self.query = query
        self.params = params


class Neo4jDriver:

    def __init__(self, host: str, credentials: Credentials):
        print(f"Connecting to Neo4j at {host}")
        self.retries = 10
        self.delay = 1
        self.driver: Driver = GraphDatabase.driver(
            f"neo4j://{host}",
            auth=(credentials.user, credentials.password),
        )

    def query(self, query: Neo4jQuery) -> Result:
        with self.driver.session() as session:
            return session.run(query.query, query.params)

    def transaction(self, queries: List[Neo4jQuery]) -> None:
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                for query in queries:
                    tx.run(query.query, query.params)
                tx.commit()

    def close(self):
        self.driver.close()
