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

    # GET CURRENT USER SETTINGS
    response = (
        supabase.table("settings")
        .select("*")
        .eq("user_email", user_email)
        .execute()
    )

    premium = False

    if response.data:

        premium = response.data[0].get(
            "premium",
            False
        )

    # IF PREMIUM ALREADY ACTIVE
    if premium == True:

        st.success(
            "🚀 Premium Account Active"
        )

        return

    # PREMIUM FEATURES
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

    # ACTIVATE BUTTON
    if st.button("Activate Premium 🚀"):

        try:

            supabase.table("settings").update({
                "premium": True
            }).eq(
                "user_email",
                user_email
            ).execute()

            st.success(
                "🎉 Premium Activated Successfully!"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Activation Failed: {e}"
            )
