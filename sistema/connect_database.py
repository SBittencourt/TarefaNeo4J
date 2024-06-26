from neo4j import GraphDatabase

uri = "neo4j+s://174f539e.databases.neo4j.io"
username = "neo4j"
password = "wpG8A2dsUo8KyftaxPbyokWkCmkCbPzKuzROdRuD0gM"

driver = GraphDatabase.driver(uri, auth=(username, password))