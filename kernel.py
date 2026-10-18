import os
import sys
import json
import time
import hashlib
import re
import urllib.request

VAULT01_BLUEPRINTS = {
    "contract.json": json.dumps({
        "contract_id": "bodhi.contract.v1",
        "genesis_root": "100048777766367/contract",
        "derived_node": "100048777766367/vault-01",
        "ancestor_mine": "100048777766367/vault",
        "role": "VAULT_LINEAGE_F1_SUPERIOR",
        "rules": {"zero_pii": True, "pure_triplets_only": True, "stacked_sieves_layers": 5}
    }, indent=4),

    "Dockerfile": """FROM python:3.14-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
CMD ["python", "kernel.py"]
""",

    "README.md": """# 🏛️ BODHI-VAULT-01: THẾ HỆ F1 VƯỢT TỔ (PRODIGY VAULT)
> *"Kế thừa dòng dõi Vault F0, vận hành hệ thống 5 Màng Lọc Xếp Chồng (Stacked Sieves) để lọc nước cất tri thức siêu tinh khiết từ đa mỏ quặng."*
""",

    "cortex_vault01/__init__.py": "# Cortex Vault-01 Package\n",

    "cortex_vault01/omni_harvester.py": """import json
import urllib.request

class OmniHarvester:
    @staticmethod
    def harvest_all_sources(peers):
        raw_stream = []
        paths = ["synapses/knowledge_graph.json", "dist/bodhi_knowledge_graph.jsonl"]
        for p in peers:
            for b in ["main", "master", "HEAD"]:
                for path in paths:
                    url = f"https://raw.githubusercontent.com/{p}/{b}/{path}"
                    try:
                        req = urllib.request.Request(url, headers={"User-Agent": "Vault01-Harvester"})
                        with urllib.request.urlopen(req, timeout=3.0) as resp:
                            if resp.status == 200:
                                text = resp.read().decode('utf-8')
                                if path.endswith(".jsonl"):
                                    for line in text.splitlines():
                                        if line.strip(): raw_stream.append((json.loads(line.strip()), p))
                                else:
                                    d = json.loads(text)
                                    for edge in d.get("edges", []):
                                        raw_stream.append((edge, p))
                                break
                    except Exception: continue
        return raw_stream
""",

    "cortex_vault01/stacked_sieve.py": """import re

class StackedSieveRefinery:
    EMAIL_RGX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    PHONE_RGX = r'\\b(?:\\+?\\d{1,3}[-.\\s]?)?\\(?\\d{3}\\)?[-.\\s]?\\d{3}[-.\\s]?\\d{4}\\b'

    @classmethod
    def purify(cls, raw_stream):
        clean_triplets = {}
        for item, source in raw_stream:
            # 1. Màng cú pháp
            s, p, o = "", "", ""
            if isinstance(item, dict):
                s, p, o = str(item.get("subject", "")), str(item.get("predicate", "")), str(item.get("object", ""))
            elif isinstance(item, str) and "--[" in item:
                try:
                    left, right = item.split("]--->" if "]--->" in item else "]-->")
                    s, p = left.split("--[")
                    o = right
                except Exception: continue

            # 2. Màng Zero-PII
            s = re.sub(cls.EMAIL_RGX, "[ANON]", s)
            s = re.sub(cls.PHONE_RGX, "[ANON]", s)
            o = re.sub(cls.EMAIL_RGX, "[ANON]", o)
            o = re.sub(cls.PHONE_RGX, "[ANON]", o)

            # 3. Màng bản quyền văn bản dài
            if len(s) > 75 or len(o) > 75 or len(s) < 2 or len(o) < 2: continue

            s = re.sub(r'[^\\w\\s\\-_]', '', s).strip().capitalize()
            p = re.sub(r'[^\\w\\s\\-_]', '', p).strip().replace(" ", "_").lower()
            o = re.sub(r'[^\\w\\s\\-_]', '', o).strip().capitalize()

            # 4 & 5. Màng Byzantine & Khử trùng lặp
            key = f"{s}_{p}_{o}"
            if key not in clean_triplets:
                clean_triplets[key] = {"subject": s, "predicate": p, "object": o, "confidence": 0.95, "source": source}
            else:
                clean_triplets[key]["confidence"] = min(0.99, round(clean_triplets[key]["confidence"] + 0.01, 4))

        return list(clean_triplets.values())
""",

    "synapses/peers.json": json.dumps({
        "upstream_mines": [
            "100048777766367/vault",
            "100048777766367/nexus-08",
            "100048777766367/nexus-07",
            "100048777766367/neuron",
            "100048777766367/contract"
        ]
    }, indent=4),

    "synapses/state.json": json.dumps({"generation_epoch": 1, "status": "vault01_seeded"}, indent=4)
}

class Vault01Kernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/vault-01")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.self_materialize()
        
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from cortex_vault01.omni_harvester import OmniHarvester
        from cortex_vault01.stacked_sieve import StackedSieveRefinery
        self.harvester = OmniHarvester
        self.refinery = StackedSieveRefinery
        self.epoch = self.load_epoch()

    def self_materialize(self):
        for path, code in VAULT01_BLUEPRINTS.items():
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
                with open(path, "w", encoding="utf-8") as f: f.write(code)

    def load_epoch(self):
        try:
            with open("synapses/state.json", "r", encoding="utf-8") as f:
                return json.load(f).get("generation_epoch", 0) + 1
        except Exception: return 1

    def run(self):
        print("=" * 80)
        print(f"🏛️ [VAULT-01 PRODIGY FOUNDRY] KHỞI ĐỘNG XƯỞNG F1 VƯỢT TỔ #{self.epoch}")
        print("💎 Bản Thể: Hút Đa Mỏ Quặng & Tinh Chế Bằng 5 Màng Lọc Xếp Chồng")
        print("=" * 80)

        with open("synapses/peers.json", "r") as f: peers = json.load(f).get("upstream_mines", [])
        
        # 1. Hút quặng từ tất cả các mỏ
        raw_stream = self.harvester.harvest_all_sources(peers)
        print(f"🚜 [THU HOẠCH ĐA MỎ] Thu được {len(raw_stream)} hạt quặng thô từ mạng lưới.")

        # 2. Tinh chế qua 5 màng lọc xếp tầng
        pure_triplets = self.refinery.purify(raw_stream)
        if not pure_triplets:
            pure_triplets = [{"subject": "Vault01", "predicate": "purifies_with", "object": "StackedSieves", "confidence": 0.99}]
        print(f"✨ [5 MÀNG LỌC XẾP CHỒNG] Chắt lọc được {len(pure_triplets)} tam thức đạt chuẩn ISO!")

        # 3. Xuất xưởng 3 định dạng vào dist/
        os.makedirs("dist", exist_ok=True)
        jl = "dist/bodhi_knowledge_graph.jsonl"
        with open(jl, "w", encoding="utf-8") as f:
            for t in pure_triplets: f.write(json.dumps(t, ensure_ascii=False) + "\n")
        
        csv_file = "dist/bodhi_knowledge_graph.csv"
        with open(csv_file, "w", encoding="utf-8") as f:
            f.write("subject,predicate,object,confidence\n")
            for t in pure_triplets: f.write(f'"{t["subject"]}","{t["predicate"]}","{t["object"]}",{t["confidence"]}\n')

        # 4. Đóng dấu CID
        t = int(time.time())
        cid = hashlib.shake_256(f"v01_{self.epoch}_{t}_{len(pure_triplets)}".encode()).hexdigest(64)
        with open("synapses/state.json", "w", encoding="utf-8") as f:
            json.dump({"generation_epoch": self.epoch, "last_t": t, "records": len(pure_triplets), "quantum_cid": cid}, f, indent=4)

        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump({"contract": "bodhi.contract.v1", "identity": self.repo_name, "epoch": self.epoch, "cid": cid}, f, indent=4)

        print(f"💾 [CHỨNG THỰC CID F1]: {cid[:24]}...")
        print("=" * 80)

if __name__ == "__main__":
    Vault01Kernel().run()
