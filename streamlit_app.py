import streamlit as st

from agents import project_agent
from agents import market_agent
from agents import risk_agent
from agents import reporting_agent

# Initialize agents
project_agent = project_agent.ProjectAgent()
market_agent = market_agent.MarketAgent()
risk_agent = risk_agent.RiskAgent()
reporting_agent = reporting_agent.ReportingAgent()

st.set_page_config(page_title="AI Risk Analyzer", layout="centered")

st.title("🧠 AI Project Risk Analyzer")
st.markdown("Enter project details and market conditions to assess risk.")

# -------------------------------
# USER INPUT
# -------------------------------

st.header("📊 Project Details")

project_id = st.text_input("Project ID", "1")

deadline = st.date_input("Deadline")
completion_date = st.date_input("Completion Date")

budget_allocated = st.number_input("Budget Allocated", value=10000)
budget_used = st.number_input("Budget Used", value=12000)

st.header("🌐 Market Conditions")

market_news_input = st.text_area(
    "Enter market news (one per line)",
    "Global supply chain disruption\nInflation rising"
)

# -------------------------------
# RUN ANALYSIS
# -------------------------------

if st.button("🚀 Analyze Risk"):

    with st.spinner("Running AI Agents..."):

        # Format project data
        project_data = {
            "project_id": project_id,
            "deadline": str(deadline),
            "completion_date": str(completion_date),
            "budget_allocated": budget_allocated,
            "budget_used": budget_used
        }

        # Convert news input into list
        market_news = [line.strip() for line in market_news_input.split("\n") if line.strip()]

        try:
            # ---------------------------
            # Run Agents
            # ---------------------------
            project_result = project_agent.analyze(project_data)
            market_result = market_agent.analyze(market_news[:2])  # limit size
            final_result = risk_agent.analyze(project_result, market_result)
            report = reporting_agent.generate_report(project_data, final_result)

            # ---------------------------
            # OUTPUT
            # ---------------------------
            st.success("✅ Analysis Complete")

            st.subheader("⚠️ Final Risk")
            st.json(final_result)

            st.subheader("📝 Report")
            st.write(report)

        except Exception as e:
            st.error(f"❌ Error: {e}")