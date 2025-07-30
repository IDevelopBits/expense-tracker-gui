import json
import time
from datetime import date
import streamlit as st
from streamlit_local_storage import LocalStorage
from expense import Expense


def create_add_form():
    expense_form = st.form("expense_form")

    local_storage = LocalStorage()

    # Initialize list in session state if it doesn't exist
    if "expenses" not in st.session_state:
        st.session_state.expenses = load_expenses(local_storage)

    with expense_form:

        col1, col2 = st.columns(2)
        with col1:
            expense_name = st.text_input("Enter your expense", placeholder="Ice Cream")
            expense_description = st.text_area("Enter description of expense", placeholder="Vanilla flavor from Rita's")
            submitted = st.form_submit_button("Submit")
        with col2:
            expense_amount = st.number_input("Enter your expense amount", value=0.00, step=0.25)
            expense_date = st.date_input("Enter the date of the expense", value=date.today(), format="MM/DD/YYYY")

        if submitted:
            expense = Expense(expense_name, expense_description, expense_date, expense_amount)
            st.session_state.expenses.append(expense)
            expenses = st.session_state.expenses
            save_expenses(local_storage, expenses)

    # Show all submitted expenses
    st.markdown(
        f"<h3 style='text-align: center;'>Expense History - Total: ${sum_expenses(st.session_state.expenses):.2f}</h3>"
        , unsafe_allow_html=True)

    with st.expander("View Expense History", expanded=False):
        for e in st.session_state.expenses:
            st.markdown(f"""
            <details>
            <summary>ID: {e.id} | <strong>{e.title}</strong> - ${e.amount:.2f} on
{e.date_.strftime("%B %d, %Y")}</summary>
            <p>{e.description}</p>
            </details>
            <hr>
            """, unsafe_allow_html=True)

    create_delete_form(local_storage, st.session_state.expenses)

    # Stores delete status after reruns
    if "delete_status" in st.session_state and "delete_message" in st.session_state:
        if st.session_state.delete_status == "success":
            st.success(st.session_state.delete_message)
        elif st.session_state.delete_status == "error":
            st.error(st.session_state.delete_message)
        # Clear after showing
        del st.session_state.delete_status
        del st.session_state.delete_message


def create_delete_form(local_storage, expenses):
    delete_form = st.form("delete_form")
    with delete_form:
        delete_id = st.text_input("Enter expense ID to delete (0 to remove all)", value=1)
        delete_button = st.form_submit_button("Delete")
        if delete_button:
            delete_id_int = int(delete_id)

            if delete_id_int == 0 and len(expenses) > 0:
                # Clear all expenses
                expenses.clear()
                save_expenses(local_storage, expenses)
                st.session_state.delete_status = "success"
                st.session_state.delete_message = "All expenses deleted successfully"
                st.rerun()
            else:
                original_len = len(expenses)
                expenses[:] = [e for e in expenses if e.id != delete_id_int]

                if len(expenses) < original_len:
                    save_expenses(local_storage, expenses)
                    st.session_state.delete_status = "success"
                    st.session_state.delete_message = "Expense deleted successfully"
                    st.rerun()
                else:
                    st.session_state.delete_status = "error"
                    st.session_state.delete_message = "Expense deleted unsuccessfully"
                    st.rerun()


def sum_expenses(expenses):
    total = sum(e.amount for e in expenses)
    return total


def save_expenses(local_storage, expenses):
    local_storage.setItem("expenses", json.dumps([e.to_dict() for e in expenses], indent=2))


def load_expenses(local_storage):
    try:
        data = json.loads(local_storage.getItem("expenses"))
    except Exception as e:
        print(e)
        return []
    expenses = [Expense.from_dict(d) for d in data]
    Expense._id_counter = max((e.id for e in expenses), default=0) + 1
    return expenses


create_add_form()
