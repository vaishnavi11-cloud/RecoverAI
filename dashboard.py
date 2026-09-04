import streamlit as st
import matplotlib.pyplot as plt


def show_dashboard(df):

    st.title("💰 RecoverAI")
    st.caption("Autonomous Intelligence for Failed Payment Recovery")

    # ---------------- METRICS ----------------

    total_recovered = df["recovered_amount"].sum()

    total_payments = len(df)

    successful_recoveries = (
        df["result"] == "SUCCESS"
    ).sum()

    success_rate = (
        successful_recoveries / total_payments
    ) * 100 if total_payments > 0 else 0

    revenue_at_risk = df["amount"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Revenue Recovered",
        f"₹{total_recovered:,}"
    )

    col2.metric(
        "⚠️ Revenue at Risk",
        f"₹{revenue_at_risk:,}"
    )

    col3.metric(
        "🎯 Recovery Success Rate",
        f"{success_rate:.1f}%"
    )

    col4.metric(
        "📊 Recovery Decisions",
        total_payments
    )

    st.divider()

    # ---------------- PERFORMANCE ----------------

    st.subheader("📈 Recovery Performance")

    recovered = total_recovered
    remaining = revenue_at_risk - total_recovered

    fig, ax = plt.subplots()

    ax.bar(
        ["Recovered Revenue", "Revenue Remaining"],
        [recovered, remaining]
    )

    ax.set_ylabel("Amount (₹)")

    st.pyplot(fig, use_container_width=True)

    st.divider()

    # ---------------- RECENT ACTIVITY ----------------

    st.subheader("🔄 Recent Recovery Activity")

    activity_df = df[
        [
            "payment_id",
            "amount",
            "failure_reason",
            "action",
            "result",
            "recovered_amount"
        ]
    ].copy()

    activity_df = activity_df.sort_values(
        by="payment_id",
        ascending=False
    )

    st.dataframe(
        activity_df,
        use_container_width=True,
        hide_index=True
    )