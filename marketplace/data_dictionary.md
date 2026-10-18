# 📖 BODHI-VAULT DATA DICTIONARY & SCHEMA SPECIFICATION
> Standard: Bodhi Clean Derivative Graph Format (Zero-PII) | Version: 1.0.0

### Schema Specification:
- **`subject`** *(String)*: Normalized entity head node.
- **`predicate`** *(String)*: Directed semantic relationship between entities.
- **`object`** *(String)*: Normalized entity tail node.
- **`confidence`** *(Float)*: Algorithmic convergence score `[0.0, 1.0]`.

### Formats Included in Package:
1. `bodhi_knowledge_graph.jsonl`: Line-delimited JSON for LlamaIndex/LangChain ingestion.
2. `bodhi_knowledge_graph.csv`: Standard comma-separated table format.
3. `neo4j_import.cypher`: Production Cypher queries for instant graph database creation.

### Legal Compliance:
- 100% Synthetic & Non-Extractive Derived Relations.
- Zero Personal Identifiable Information (Zero-PII).
- Permitted for full commercial, enterprise, and research usage.
