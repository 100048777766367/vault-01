import os
import json

class MarketPackager:
    @staticmethod
    def export_all(triplets, output_dir="dist"):
        os.makedirs(output_dir, exist_ok=True)
        jsonl_path = os.path.join(output_dir, "bodhi_knowledge_graph.jsonl")
        csv_path = os.path.join(output_dir, "bodhi_knowledge_graph.csv")
        cypher_path = os.path.join(output_dir, "neo4j_import.cypher")

        # 1. Xuất file .jsonl (Chuẩn cho LLM & GraphRAG)
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for item in triplets:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # 2. Xuất file .csv (Chuẩn bảng tính)
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("subject,predicate,object,confidence\n")
            for item in triplets:
                s = item["subject"].replace('"', '""')
                p = item["predicate"].replace('"', '""')
                o = item["object"].replace('"', '""')
                f.write(f'"{s}","{p}","{o}",{item["confidence"]}\n')

        # 3. Xuất file .cypher (Nạp thẳng vào Neo4j bằng 1 click)
        with open(cypher_path, "w", encoding="utf-8") as f:
            f.write("// Bodhi-Mesh Knowledge Graph Import for Neo4j\n")
            for item in triplets:
                s = item["subject"].replace('"', '\\"')
                p = item["predicate"].upper().replace(" ", "_").replace("-", "_")
                o = item["object"].replace('"', '\\"')
                f.write(f'MERGE (s:Entity {{name: "{s}"}}) MERGE (o:Entity {{name: "{o}"}}) MERGE (s)-[:{p}]->(o);\n')

        print(f"📦 [ĐÓNG GÓI XUẤT XƯỞNG] Đã tạo thành phẩm: .jsonl, .csv, .cypher ({len(triplets)} bản ghi)!")
        return {"jsonl": jsonl_path, "csv": csv_path, "cypher": cypher_path}
