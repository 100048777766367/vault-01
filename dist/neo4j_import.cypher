// Bodhi-Mesh Knowledge Graph Import for Neo4j
MERGE (s:Entity {name: "BodhiMesh"}) MERGE (o:Entity {name: "SelfSustainingIntelligence"}) MERGE (s)-[:EMBODIES]->(o);
MERGE (s:Entity {name: "Contract"}) MERGE (o:Entity {name: "InvariantZeroSPOF"}) MERGE (s)-[:ENFORCES]->(o);
MERGE (s:Entity {name: "Vault"}) MERGE (o:Entity {name: "CleanKnowledgeGraphs"}) MERGE (s)-[:REFINES]->(o);
MERGE (s:Entity {name: "Nexus"}) MERGE (o:Entity {name: "MultiDimensionalSignals"}) MERGE (s)-[:TRANSMUTES]->(o);
