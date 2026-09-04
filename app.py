import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

from main import run_recovery_simulation
from dashboard import show_dashboard
from explanation_engine import (
    explain_decision,
    calculate_confidence,
    get_confidence_factors,
    get_decision_rule,
    calculate_priority
)


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="RecoverAI",
    page_icon="💰",
    layout="wide"
)


# ---------------- SIDEBAR ----------------

st.sidebar.title("💰 RecoverAI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📊 Analytics",
        "🧠 AI Insights",
        "🤖 Decision Engine",
        "📋 Payment Details"
    ]
)


# ---------------- LOAD DATA ----------------

if not os.path.exists("audit_log.json"):
    st.warning("No recovery data found. Run a recovery simulation first.")
    st.stop()

with open("audit_log.json", "r") as file:
    audit_data = json.load(file)

df = pd.DataFrame(audit_data)


# ==================================================
# 🏠 DASHBOARD
# ==================================================

if page == "🏠 Dashboard":

    show_dashboard(df)

    if st.button("🚀 Run Recovery Simulation"):
        run_recovery_simulation()
        st.success("New recovery simulation completed!")
        st.rerun()

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Recovery Report",
        data=csv,
        file_name="recovery_report.csv",
        mime="text/csv"
    )


# ==================================================
# 📊 ANALYTICS
# ==================================================

elif page == "📊 Analytics":

    st.title("📊 Recovery Analytics")

    chart1, chart2 = st.columns(2)

    with chart1:

        st.write("### Failure Reasons")

        failure_counts = df["failure_reason"].value_counts()

        fig, ax = plt.subplots()

        failure_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_xlabel("Failure Reason")
        ax.set_ylabel("Number of Payments")

        st.pyplot(fig)

    with chart2:

        st.write("### Agent Actions")

        action_counts = df["action"].value_counts()

        fig, ax = plt.subplots()

        action_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_xlabel("Agent Action")
        ax.set_ylabel("Number of Decisions")

        st.pyplot(fig)


# ==================================================
# 🧠 AI INSIGHTS
# ==================================================

elif page == "🧠 AI Insights":

    st.title("🧠 AI Recovery Insights")

    col1, col2, col3 = st.columns(3)

    with col1:

        most_common_failure = (
            df["failure_reason"]
            .value_counts()
            .idxmax()
        )

        st.info(
            f"📊 **Most Common Failure**\n\n"
            f"{most_common_failure}"
        )

    with col2:

        successful_actions = df[
            df["result"] == "SUCCESS"
        ]["action"]

        if not successful_actions.empty:

            best_action = (
                successful_actions
                .value_counts()
                .idxmax()
            )

            st.success(
                f"🤖 **Most Effective Action**\n\n"
                f"{best_action}"
            )

        else:

            st.warning(
                "No successful recovery actions yet."
            )

    with col3:

        lost_revenue = df[
            df["result"] == "FAILED"
        ]["amount"].sum()

        st.warning(
            f"💰 **Revenue Still Lost**\n\n"
            f"₹{lost_revenue}"
        )
# ==================================================
# 🤖 DECISION ENGINE
# ==================================================

elif page == "🤖 Decision Engine":

    st.title("🤖 AI Decision Explanation")

    st.caption(
        "RecoverAI analyzes failed payments, evaluates customer context, "
        "selects a recovery strategy, and explains every decision."
    )

    st.info(
        "🤖 Select a payment below to inspect RecoverAI's "
        "decision-making process."
    )

    payment_ids = df["payment_id"].tolist()

    selected_payment_id = st.selectbox(
        "Select a Payment",
        payment_ids
    )

    payment_data = df[
        df["payment_id"] == selected_payment_id
    ].iloc[0]

    priority = calculate_priority(payment_data)

    st.subheader("📋 Payment Context")
    priority_col1, priority_col2 = st.columns(2)

    with priority_col1:
        st.metric(
            "🚨 Recovery Priority Score",
            f"{priority}/90"
        )

    with priority_col2:

        if priority >= 60:
            st.error("🔴 HIGH PRIORITY")

        elif priority >= 35:
            st.warning("🟡 MEDIUM PRIORITY")

        else:
            st.success("🟢 LOW PRIORITY")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Amount",
        f"₹{payment_data['amount']}"
    )

    col2.metric(
        "🔁 Retry Count",
        payment_data["retry_count"]
    )

    col3.metric(
        "👤 Customer History",
        payment_data["customer_history"]
    )

    st.write(
        f"**Failure Reason:** {payment_data['failure_reason']}"
    )

    st.write(
        f"**Previous Successful Payments:** "
        f"{payment_data['previous_successful_payments']}"
    )

    st.divider()

    st.subheader("🔄 Decision Flow")

    flow_col1, flow_col2, flow_col3, flow_col4 = st.columns(4)

    with flow_col1:
        st.info("❌ Payment Failed")

    with flow_col2:
        st.info(
            f"🔍 Reason\n\n"
            f"{payment_data['failure_reason']}"
        )

    with flow_col3:
        st.info(
            f"👤 Customer\n\n"
            f"{payment_data['customer_history']}"
        )

    with flow_col4:
        st.success(
            f"🤖 Decision\n\n"
            f"{payment_data['action']}"
        )

    st.subheader("🤖 Agent Decision")

    confidence = calculate_confidence(
        payment_data,
        payment_data["action"]
    )
    factors = get_confidence_factors(
        payment_data,
        payment_data["action"]
    )

    st.metric(
        "🎯 Decision Confidence",
        f"{confidence}%"
    )
    
    
    st.subheader("📊 Confidence Breakdown")

    for factor, points in factors:

        if points >= 0:
            st.write(
                f"✅ **{factor}**: +{points} points"
            )

        else:
            st.write(
                f"⚠️ **{factor}**: {points} points"
            )

    st.divider()

    st.success(
        f"🎯 Final Decision Confidence: **{confidence}%**"
    )

    explanation = explain_decision(
        payment_data,
        payment_data["action"]
    )
    decision_rule = get_decision_rule(
        payment_data,
        payment_data["action"]
    )

    st.subheader("🧠 Why did RecoverAI choose this?")

    st.info(explanation)
    st.subheader("📌 Decision Rule Applied")

    st.code(decision_rule)
    st.divider()

    st.subheader("📈 Predicted Recovery Chance")

    success_probability = payment_data["success_probability"]

    st.metric(
        "🤖 Predicted Success Probability",
        f"{success_probability * 100:.0f}%"
    )

    st.progress(success_probability)
    st.divider()


    st.subheader("📊 Recovery Outcome")
    st.divider()

    st.subheader("💡 AI Recommendation")

    action = payment_data["action"]
    result = payment_data["result"]

    if action == "RETRY_PAYMENT":
        st.info(
            "🔄 RecoverAI recommends retrying the payment "
            "because the failure may be temporary."
        )

    elif action == "SEND_PAYMENT_LINK":
        st.info(
            "🔗 RecoverAI recommends sending a payment link "
            "so the customer can complete the payment later."
        )

    elif action == "OFFER_ALTERNATIVE_METHOD":
        st.info(
            "💳 RecoverAI recommends offering another payment "
            "method to increase the chance of recovery."
        )

    else:
        st.warning(
            "🛑 RecoverAI recommends stopping further recovery "
            "attempts because the probability of success is low."
        )

    col1, col2 = st.columns(2)

    col1.metric(
        "Result",
        payment_data["result"]
    )

    col2.metric(
        "Recovered Amount",
        f"₹{payment_data['recovered_amount']}"
    )
    st.divider()

    st.subheader("🚨 Recovery Priority Queue")
    high_priority = 0
    medium_priority = 0
    low_priority = 0

    for _, payment in df.iterrows():

        payment_priority = calculate_priority(payment)

        if payment_priority >= 60:
            high_priority += 1

        elif payment_priority >= 35:
            medium_priority += 1

        else:
            low_priority += 1


    priority_col1, priority_col2, priority_col3 = st.columns(3)

    priority_col1.metric(
        "🔴 High Priority",
        high_priority
    )

    priority_col2.metric(
        "🟡 Medium Priority",
        medium_priority
    )

    priority_col3.metric(
        "🟢 Low Priority",
        low_priority
    )

    priority_df = df.copy()

    priority_df["priority_score"] = priority_df.apply(
        calculate_priority,
        axis=1
    )

    priority_df = priority_df.sort_values(
        by="priority_score",
        ascending=False
    )

    priority_display = priority_df[
        [
            "payment_id",
            "amount",
            "failure_reason",
            "customer_history",
            "action",
            "priority_score"
        ]
    ]

    st.dataframe(
        priority_display,
        use_container_width=True
    )

# ==================================================
# 📋 PAYMENT DETAILS
# ==================================================

elif page == "📋 Payment Details":

    st.title("📋 Payment Recovery Details")

    display_df = df[
        [
            "payment_id",
            "amount",
            "failure_reason",
            "action",
            "result",
            "recovered_amount"
        ]
    ]

    selected_reason = st.selectbox(
        "Filter by Failure Reason",
        ["All"] + list(
            df["failure_reason"].unique()
        )
    )

    search_payment = st.text_input(
        "🔍 Search by Payment ID",
        placeholder="Example: PAY007"
    )

    if selected_reason != "All":

        display_df = display_df[
            display_df["failure_reason"]
            == selected_reason
        ]

    if search_payment:

        display_df = display_df[
            display_df["payment_id"]
            .str.contains(
                search_payment,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        display_df,
        use_container_width=True
    )

    csv = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Payment Data",
        data=csv,
        file_name="recovery_audit.csv",
        mime="text/csv"
    )