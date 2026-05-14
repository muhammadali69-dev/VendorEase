import streamlit as st
import razorpay

from supabase_client import supabase

RAZORPAY_KEY_ID = st.secrets["RAZORPAY_KEY_ID"]
RAZORPAY_SECRET = st.secrets["RAZORPAY_SECRET"]

client = razorpay.Client(
    auth=(
        RAZORPAY_KEY_ID,
        RAZORPAY_SECRET
    )
)


def premium_upgrade():

    st.markdown("---")

    st.subheader("💎 VendorEase Premium")

    settings = supabase.table("settings").select("*").eq(
        "user_email",
        st.session_state["user"].email
    ).execute()

    if settings.data and settings.data[0].get("premium"):

        st.success("🚀 Premium Account Active")

        return

    st.info(
        """
Upgrade to Premium for:

✅ Unlimited transactions  
✅ Advanced analytics  
✅ AI business insights  
✅ Inventory intelligence  
✅ Premium reports  
"""
    )

    st.write("### ₹99 / month")

    if st.button("Activate Premium 🚀"):

        user = st.session_state.get("user")

        if not user:

            st.error("Please login first")
            return

        # TEST PAYMENT SIMULATION

        supabase.table("settings").update({
            "premium": True
        }).eq(
            "user_email",
            user.email
        ).execute()

        st.success(
            "🎉 Payment Successful! Premium Activated."
        )
