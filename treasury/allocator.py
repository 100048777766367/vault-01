import os
import json

LEDGER_FILE = "treasury/ledger.json"

class TreasuryAllocator:
    @staticmethod
    def record_harvest(node_id, items_count):
        data = {"total_revenue_usd": 0.0, "reserve_buffer_usd": 0.0, "node_contributions": {}}
        if os.path.exists(LEDGER_FILE):
            try:
                with open(LEDGER_FILE, "r", encoding="utf-8") as f: data = json.load(f)
            except Exception: pass

        contrib = data["node_contributions"].get(node_id, 0)
        data["node_contributions"][node_id] = contrib + items_count

        with open(LEDGER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def allocate_40_30_30(revenue_usd):
        infra_budget = round(revenue_usd * 0.40, 2)   # 40% chi phí máy chủ, Actions
        reserve_fund = round(revenue_usd * 0.30, 2)   # 30% quỹ dự phòng rủi ro
        node_rewards = round(revenue_usd * 0.30, 2)   # 30% nuôi dưỡng các nút thợ
        return {
            "infrastructure_40": infra_budget,
            "reserve_30": reserve_fund,
            "rewards_30": node_rewards
        }
