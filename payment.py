import streamlit as st

from supabase_client import supabase


def premium_upgrade():

    st.markdown("---")

    st.subheader("💎 VendorEase Premium")

    user = st.session_state.get("user")

    if not user:

        st.error("Please login first")
        return

    user_email = user.email

    st.write("Premium Plan — ₹99/month")

    if st.button("Activate Premium 🚀"):

        # FORCE UPDATE

        supabase.table("settings").update({
            "premium": True
        }).eq(
            "user_email",
            user_email
        ).execute()

        st.success("🎉 Premium Activated!")

        # FORCE PAGE REFRESH
        st.session_state["premium_refresh"] = True

        st.rerun()
