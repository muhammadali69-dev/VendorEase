import streamlit as st

from supabase_client import supabase


def premium_upgrade():

    st.markdown("---")

    st.subheader("💎 VendorEase Premium")

    user = st.session_state.get("user")

    if not user:

        st.error("Please login first")
        return

    # CORRECT EMAIL ACCESS
    user_email = user.user_metadata["email"]

    st.write(f"Logged in as: {user_email}")

   if st.button("Activate Premium 🚀"):

    st.write("BUTTON WORKING")

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
        except Exception as e:

            st.error(
                f"ERROR: {e}"
            )
