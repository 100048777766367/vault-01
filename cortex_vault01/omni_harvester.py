import json
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
