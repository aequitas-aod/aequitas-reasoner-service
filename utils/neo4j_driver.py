import time
from typing import LiteralString

from neo4j import GraphDatabase, Driver, Result
from neo4j.exceptions import ServiceUnavailable


class Credentials:
    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password


class Neo4jDriver:

    def __init__(self, host: str, credentials: Credentials):
        print(f"Connecting to Neo4j at {host}")
        self.retries = 10
        self.delay = 1
        self.driver: Driver = GraphDatabase.driver(
            f"neo4j://{host}",
            auth=(credentials.user, credentials.password),
        )

    def query(self, query: str, **kwargs: dict) -> Result:
        for attempt in range(self.retries):
            try:
                with self.driver.session() as session:
                    return session.run(query, **kwargs)
            except ServiceUnavailable as e:
                if attempt < self.retries - 1:
                    time.sleep(self.delay)
                else:
                    raise e

    def close(self):
        self.driver.close()