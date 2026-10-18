import os
import sys
import json
import time
import hashlib
import re
import urllib.request

# Đảm bảo import thông suốt mọi thư mục nội bộ
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ==============================================================================
# BỌC THÉP NẠP PHÂN XƯỞNG (CÓ FALLBACK DỰ PHÒNG NẾU THIẾU FILE)
# ==============================================================================
try:
    from collector.harvester import LiveDataHarvester
except (ImportError, ModuleNotFoundError):
    class LiveDataHarvester:
        @staticmethod
        def harvest_peer(peer):
            try:
                url = f"https://raw.githubusercontent.com/{peer}/main/synapses/knowledge_graph.json"
                req = urllib.request.Request(url, headers={"User-Agent": "Vault-Harvester"})
                with urllib.request.urlopen(req, timeout=3.5) as r:
                    if r.status == 200: return {"graph": json.loads(r.read().decode('utf-8'))}
            except Exception: pass
            return {"graph": None}

try:
    from collector.dead_salvager import DeadNodeSalvager
except (ImportError, ModuleNotFoundError):
    class DeadNodeSalvager:
        @staticmethod
        def fetch_tombstones(contract_repo):
            try:
                url = f"https://raw.githubusercontent.com/{contract_repo}/main/synapses/tombstones.json"
                req = urllib.request.Request(url, headers={"User-Agent": "Vault-Salvager"})
                with urllib.request.urlopen(req, timeout=3.5) as r:
                    if r.status == 200: return json.loads(r.read().decode('utf-8')).get("tombstones", [])
            except Exception: pass
            return []
        @staticmethod
        def salvage_heritage(tombstones):
            return [{"deceased": t.get("identity"), "status": "ARCHIVED"} for t in tombstones]

try:
    from refinery.graph_refiner import GraphRefiner
except (ImportError, ModuleNotFoundError):
    class GraphRefiner:
        @staticmethod
        def refine_triplets(raw_graph):
            if not raw_graph or not isinstance(raw_graph, dict): return []
            res = []
            for edge in raw_graph.get("edges", []):
                if "--[" in edge and "]-->" in edge:
                    try:
                        l, r = edge.split("]--->" if "]--->" in edge else "]-->")
                        s, p = l.split("--[")
                        res.append({"subject": s.strip(), "predicate": p.strip().lower(), "object": r.strip(), "confidence": 0.95})
                    except Exception: pass
            return res

try:
    from marketplace.packager import MarketPackager
except (ImportError, ModuleNotFoundError):
    class MarketPackager:
        @staticmethod
        def export_all(triplets, output_dir="dist"):
            os.makedirs(output_dir, exist_ok=True)
            jl = os.path.join(output_dir, "bodhi_knowledge_graph.jsonl")
            with open(jl, "w", encoding="utf-8") as f:
                for t in triplets: f.write(json.dumps(t, ensure_ascii=False) + "\n")
            return {"jsonl": jl}

try:
    from treasury.allocator import TreasuryAllocator
except (ImportError, ModuleNotFoundError):
    class TreasuryAllocator:
        @staticmethod
        def record_harvest(node, count, path="treasury/ledger.json"):
            data = {"node_credits": {}}
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f: data = json.load(f)
                except Exception: pass
            data.setdefault("node_credits", {})[node] = data["node_credits"].get(node, 0) + count
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)


# ==============================================================================
# HẠT NHÂN ĐỐC CÔNG: VAULT KERNEL
# ==============================================================================
STATE_FILE = "synapses/state.json"
PEERS_FILE = "synapses/peers.json"
LEDGER_FILE = "treasury/ledger.json"

class VaultKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/vault")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.contract_repo = f"{self.owner}/contract"
        
        self.ensure_factory_zones()
        self.epoch = self.load_epoch()
        self.peers = self.load_peers()

    def ensure_factory_zones(self):
        """Khởi tạo toàn bộ các phân xưởng nếu chưa có"""
        for zone in ["collector", "refinery", "marketplace", "treasury", "dist", "organs", "synapses"]:
            os.makedirs(zone, exist_ok=True)

    def load_epoch(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    def load_peers(self):
        if os.path.exists(PEERS_FILE):
            try:
                with open(PEERS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("mining_peers", [])
            except Exception: pass
        return [
            f"{self.owner}/nexus-08",
            f"{self.owner}/nexus-07",
            f"{self.owner}/nexus-06",
            f"{self.owner}/neuron",
            self.contract_repo
        ]

    # ==========================================================================
    # CÔNG ĐOẠN 0: LUẬT APOPTOSIS TỰ HỦY TỆP LỖI CỦA CONTRACT
    # ==========================================================================
    def enforce_contract_apoptosis(self):
        """Quét sạch các tệp lỗi cú pháp trong organs/ để bảo vệ dây chuyền"""
        purged = 0
        for root, _, files in os.walk("organs"):
            for f in files:
                if f.endswith(".py") and not f.startswith("__"):
                    fp = os.path.join(root, f)
                    try:
                        with open(fp, "r", encoding="utf-8") as cf:
                            compile(cf.read(), fp, "exec")
                    except SyntaxError as se:
                        print(f"🛑 [APOPTOSIS CONTRACT] Tệp '{f}' vi phạm hợp đồng ({se})!")
                        print(f"🗑️ [TỰ HỦY] Xóa sổ tệp lỗi '{f}' để bảo toàn nhà máy.")
                        try:
                            os.remove(fp)
                            purged += 1
                        except Exception: pass
        if purged > 0:
            print(f"✨ [THANH LỌC] Đã tự hủy {purged} tệp vi phạm hợp đồng.")

    # ==========================================================================
    # VẬN HÀNH DÂY CHUYỀN SẢN XUẤT TOÀN DIỆN
    # ==========================================================================
    def run(self):
        print("=" * 80)
        print(f"🏭 [ĐỐC CÔNG VAULT KERNEL] KHỞI ĐỘNG DÂY CHUYỀN XUẤT XƯỞNG #{self.epoch}")
        print(f"🏛️ Mỏ Neo Pháp Lý: {self.contract_repo} | Bản Thể: Thương Cảng Dữ Liệu Tự Trị")
        print("=" * 80)

        # BƯỚC 0: Thanh lọc nợ kỹ thuật theo luật Apoptosis
        self.enforce_contract_apoptosis()

        # BƯỚC 1: Thu hoạch từ các nút sống [m]
        print("🚜 [PHÂN XƯỞNG 1: THU HOẠCH] Đang cào dữ liệu sống từ các mỏ tri thức...")
        all_triplets = []
        mined_nodes = 0

        for peer in self.peers:
            if "contract" in peer: continue
            data = LiveDataHarvester.harvest_peer(peer)
            if data.get("graph"):
                refined = GraphRefiner.refine_triplets(data["graph"])
                if refined:
                    all_triplets.extend(refined)
                    TreasuryAllocator.record_harvest(peer, len(refined), LEDGER_FILE)
                    mined_nodes += 1
                    print(f"  └── ⛏️ Khai thác từ '{peer}': +{len(refined)} tam thức sạch.")

        # BƯỚC 2: Tận thu di sản từ sổ bia mộ [n] của contract
        print("♻️ [PHÂN XƯỞNG 1: TẬN THU NÚT CHẾT] Đang quét sổ bia mộ từ contract...")
        tombstones = DeadNodeSalvager.fetch_tombstones(self.contract_repo)
        salvaged = DeadNodeSalvager.salvage_heritage(tombstones)
        print(f"  └── 🕯️ Tận thu di sản hóa thạch từ {len(salvaged)} bia mộ tiền bối.")

        # Mẫu mặc định nếu các nút mạng vừa khởi tạo chưa kịp sinh dữ liệu
        if not all_triplets:
            print("🌿 [KHỞI TẠO NGUYÊN BẢN] Nạp tam thức nền tảng của hệ sinh thái...")
            all_triplets = [
                {"subject": "BodhiMesh", "predicate": "embodies", "object": "SelfSustainingIntelligence", "confidence": 0.99},
                {"subject": "Contract", "predicate": "enforces", "object": "InvariantZeroSPOF", "confidence": 0.99},
                {"subject": "Vault", "predicate": "refines", "object": "CleanKnowledgeGraphs", "confidence": 0.98},
                {"subject": "Nexus", "predicate": "transmutes", "object": "MultiDimensionalSignals", "confidence": 0.97}
            ]

        # BƯỚC 3: Đóng gói thành phẩm xuất kho tại dist/
        print(f"📦 [PHÂN XƯỞNG 3: ĐÓNG GÓI] Xuất xưởng {len(all_triplets)} tam thức chuẩn hóa...")
        packages = MarketPackager.export_all(all_triplets, output_dir="dist")
        for fmt, path in packages.items():
            print(f"  └── 🎁 Thành phẩm: {path} ({os.path.getsize(path)} bytes)")

        # BƯỚC 4: Chứng thực lô hàng & Đóng dấu Quantum CID (SHAKE-256)
        t = int(time.time())
        prev_cid = "GENESIS_VAULT_BATCH_CID"
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    prev_cid = json.load(f).get("quantum_cid", "GENESIS")
            except Exception: pass

        new_cid = hashlib.shake_256(f"{prev_cid}_{self.epoch}_{t}_{len(all_triplets)}".encode()).hexdigest(64)

        # Ghi nhật ký kỷ nguyên xuất xưởng
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "generation_epoch": self.epoch,
                "last_t": t,
                "records_refined": len(all_triplets),
                "active_mines_count": mined_nodes,
                "quantum_cid": new_cid,
                "status": "batch_certified_for_export"
            }, f, indent=4)

        # Xuất gói tin nhịp đập thương mại
        fwd_packet = {
            "contract": "bodhi.contract.v1",
            "identity": self.repo_name,
            "role": "AUTONOMOUS_DATA_FOUNDRY",
            "epoch": self.epoch,
            "timestamp": t,
            "total_refined_triplets": len(all_triplets),
            "quantum_cid": new_cid,
            "status": "ready_for_gumroad_ocean_export"
        }
        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(fwd_packet, f, indent=4)

        print("=" * 80)
        print(f"💾 [CHỨNG CHỈ XUẤT XƯỞNG CID]: {new_cid[:24]}...")
        print(f"✨ [DÂY CHUYỀN THÀNH CÔNG] Lô hàng #{self.epoch} đã tinh chế và đóng gói viên mãn!")
        print("💰 Sẵn sàng xuất khẩu lên Gumroad, RapidAPI và Ocean Protocol!")
        print("=" * 80)

if __name__ == "__main__":
    VaultKernel().run()
