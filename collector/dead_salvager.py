import json
import urllib.request

class DeadNodeSalvager:
    """Tận thu dữ liệu của các nút đã 404 để chuyển hóa thành tài sản thương mại"""
    @staticmethod
    def fetch_tombstones(contract_repo="100048777766367/contract"):
        url = f"https://raw.githubusercontent.com/{contract_repo}/main/synapses/tombstones.json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Vault-Salvager"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    return data.get("tombstones", [])
        except Exception: pass
        return []

    @staticmethod
    def salvage_heritage(tombstone_list):
        salvaged_assets = []
        for t in tombstone_list:
            salvaged_assets.append({
                "deceased_node": t.get("identity"),
                "epoch_lost": t.get("declared_dead_epoch", 0),
                "salvage_status": "HERITAGE_ARCHIVED"
            })
        return salvaged_assets
