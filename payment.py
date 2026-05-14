import streamlit as st

from supabase_client import supabase


def premium_upgrade():

    st.markdown("---")

    st.subheader("💎 VendorEase Premium")

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

    user = st.session_state.get("user")

    if not user:

        st.error("Please login first")
        return

    user_email = user.email

    if st.button("Activate Premium 🚀"):

        # FORCE PREMIUM
        supabase.table("settings").update({
            "premium": True
        }).eq(
            "user_email",
            user_email
        ).execute()

        st.success(
            "🎉 Premium Activated!"
        )

        st.write(
            "Refresh the page to see Premium status."
        )
