#from core.orchestrator import RiskOrchestrator
from core import orchestrator

orchestrator = orchestrator.RiskOrchestrator()

results = orchestrator.run()

print("\n\n========== FINAL RESULTS ==========\n")

for r in results:
    print(f"\n📌 Project {r['project_id']}")
    
    print("\n⚠️ Final Risk:")
    print(r["final_risk"])

    print("\n📝 Report:")
    print(r["report"])

    print("\n" + "="*40)