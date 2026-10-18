from refinery.pii_cleaner import PiiSanitizer

class GraphRefiner:
    """Chắt lọc các bộ ba (Subject, Predicate, Object) thuần túy toán học"""
    @staticmethod
    def refine_triplets(raw_graph):
        if not raw_graph or not isinstance(raw_graph, dict):
            return []

        refined = []
        edges = raw_graph.get("edges", [])

        for edge in edges:
            if "--[" in edge and "]-->" in edge:
                try:
                    left, right = edge.split("]--->" if "]--->" in edge else "]-->")
                    subj, pred = left.split("--[")
                    subj = PiiSanitizer.sanitize_text(subj.strip())
                    pred = PiiSanitizer.sanitize_text(pred.strip().lower())
                    obj = PiiSanitizer.sanitize_text(right.strip())

                    if subj and pred and obj:
                        refined.append({
                            "subject": subj,
                            "predicate": pred,
                            "object": obj,
                            "confidence": 0.95
                        })
                except Exception: continue
        return refined
