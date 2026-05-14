import streamlit as st

from supabase_client import supabase


def premium_upgrade():

    st.markdown("---")

    st.subheader("💎 VendorEase Premium")

    user = st.session_state.get("user")

    st.write("USER:", user)

    if not user:

        st.error("No logged in user")
        return

    user_email = user.email

    st.write("EMAIL:", user_email)

    if st.button("Activate Premium 🚀"):

        st.write("BUTTON CLICKED")

        try:

            response = (
                supabase.table("settings")
                .update({
                    "premium": True
                })
                .eq(
                    "user_email",
                    user_email
                )
                .execute()
            )

            st.write(response)

            st.success(
                "Premium Activated!"
            )

        except Exception as e:

            st.error(
                f"ERROR: {e}"
            )
