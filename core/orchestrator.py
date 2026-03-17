import json
import os

from agents import project_agent
from agents import market_agent
from agents import risk_agent
from agents import reporting_agent


class RiskOrchestrator:
    def __init__(self):
        self.project_agent = project_agent.ProjectAgent()
        self.market_agent = market_agent.MarketAgent()
        self.risk_agent = risk_agent.RiskAgent()
        self.reporting_agent = reporting_agent.ReportingAgent()

        # Absolute base directory
        self.BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

    # -------------------------------
    # Data Loaders
    # -------------------------------
    def load_projects(self):
        path = os.path.join(self.BASE_DIR, "data", "projects.json")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing file: {path}")

        with open(path, "r") as f:
            return json.load(f)

    def load_market(self):
        path = os.path.join(self.BASE_DIR, "data", "market.json")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing file: {path}")

        with open(path, "r") as f:
            return json.load(f)

    # -------------------------------
    # Main Pipeline
    # -------------------------------
    def run(self):
        results = []  # ALWAYS initialize

        # -------------------------------
        # Load Data
        # -------------------------------
        try:
            projects = self.load_projects()
            market_data = self.load_market()
        except Exception as e:
            print(f"❌ Data loading error: {e}")
            return []  # never return None

        # -------------------------------
        # Prepare Market Data
        # -------------------------------
        market_news = [
            item.get("news", "") for item in market_data
        ][:2]  # limit size (LLM stability)

        # -------------------------------
        # Market Agent (run once)
        # -------------------------------
        try:
            print("\n🔵 Running Market Analysis...")
            market_result = self.market_agent.analyze(market_news)
        except Exception as e:
            print(f"❌ Market agent failed: {e}")
            market_result = {
                "market_risk": "UNKNOWN",
                "risk_score": 0.5,
                "affected_areas": [],
                "summary": "Market analysis failed"
            }

        # -------------------------------
        # Process Each Project
        # -------------------------------
        for project in projects:
            project_id = project.get("project_id", "Unknown")
            print(f"\n🟢 Processing Project {project_id}...")

            # ---------------------------
            # Project Agent
            # ---------------------------
            try:
                project_result = self.project_agent.analyze(project)
            except Exception as e:
                print(f"❌ Project agent failed: {e}")
                project_result = {
                    "delay_risk": False,
                    "budget_risk": False,
                    "risk_level": "UNKNOWN",
                    "summary": "Project analysis failed"
                }

            # ---------------------------
            # Risk Agent
            # ---------------------------
            try:
                final_result = self.risk_agent.analyze(
                    project_result, market_result
                )
            except Exception as e:
                print(f"❌ Risk agent failed: {e}")
                final_result = {
                    "final_risk_score": 0.5,
                    "risk_level": "UNKNOWN",
                    "key_factors": [],
                    "justification": "Risk calculation failed"
                }

            # ---------------------------
            # Reporting Agent
            # ---------------------------
            try:
                report = self.reporting_agent.generate_report(
                    project, final_result
                )
            except Exception as e:
                print(f"❌ Reporting agent failed: {e}")
                report = "Report generation failed."

            # ---------------------------
            # Store Result
            # ---------------------------
            results.append({
                "project_id": project_id,
                "project_analysis": project_result,
                "market_analysis": market_result,
                "final_risk": final_result,
                "report": report
            })

        # -------------------------------
        # FINAL RETURN (IMPORTANT FIX)
        # -------------------------------
        return results if results else []


# -------------------------------
# Debug Run
# -------------------------------
if __name__ == "__main__":
    orchestrator = RiskOrchestrator()
    output = orchestrator.run()

    print("\n\n===== FINAL OUTPUT =====")

    for item in output:
        print("\n----------------------")
        print(f"Project {item['project_id']}")
        print("Risk:", item["final_risk"])
        print("Report:", item["report"])