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

        try:

            # UPDATE DATABASE
            supabase.table("settings").update({
                "premium": True
            }).eq(
                "user_email",
                user_email
            ).execute()

            # FORCE SESSION UPDATE
            st.session_state["premium"] = True

            st.success(
                "🎉 Premium Activated Successfully!"
            )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

    # SHOW ACTIVE STATUS
    settings = (
        supabase.table("settings")
        .select("*")
        .eq("user_email", user_email)
        .execute()
    )

    if settings.data:

        if settings.data[0].get("premium") == True:

            st.success("🚀 Premium Account Active")
