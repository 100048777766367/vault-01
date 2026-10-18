import json
import urllib.request

class LiveDataHarvester:
    """Thu thập đồ thị tri thức và telemetry từ các nút mạng đang sống"""
    @staticmethod
    def harvest_peer(peer_repo):
        # 1. Hút đồ thị tri thức
        graph_url = f"https://raw.githubusercontent.com/{peer_repo}/main/synapses/knowledge_graph.json"
        graph_data = None
        try:
            req = urllib.request.Request(graph_url, headers={"User-Agent": "Vault-Harvester"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                if resp.status == 200:
                    graph_data = json.loads(resp.read().decode('utf-8'))
        except Exception: pass

        # 2. Hút gói tin nhịp đập
        forward_url = f"https://raw.githubusercontent.com/{peer_repo}/main/synapse_forward.json"
        forward_data = None
        try:
            req = urllib.request.Request(forward_url, headers={"User-Agent": "Vault-Harvester"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                if resp.status == 200:
                    forward_data = json.loads(resp.read().decode('utf-8'))
        except Exception: pass

        return {"graph": graph_data, "forward": forward_data}
