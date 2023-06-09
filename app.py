
#importing the packages
import calendar
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

#auth
credentials = {
        "usernames":{
            "jsmith92":{
                "name":"john smith",
                "password":"$2b$12$TSuKwWML0EpbohBQgHx4p8E5q"
                },
            "tturner":{
                "name":"timmy turner",
                "password":"$2b$12$asdaUduuibuEIyBUBHASD896a"
                }            
            }
        }
# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:

    



    #-----settings
    incomes =["Salary","Blogs","Other Income"]
    expenses =["Rent","Utilities","Groceries","Car","Other Expenses","Savings"]
    currency ="INR"
    page_title ="Income and expense tracker"
    page_icon=":money_with_wings"
    layout="centered"
    #-------------

    st.set_page_config(page_title=page_title, page_icon=page_icon,layout=layout)
    st.title(page_title+""+page_icon)


    #Drop Down Values
    years=[datetime.today(),datetime.today().year+1]
    months=list(calendar.month_name[1:])

    #Nav menu
    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"Welcome {name}")
    selected=option_menu(
        menu_title=None,
        options=["Data Entry","Data Visualisation"],
        icons=["pencil-fill","bar-chart-fill"],
        orientation="horizontal",
    )


    #form input
    st.header(f"Data Entry in {currency}💵")
    with st.form("entry_form",clear_on_submit=True):
        col1,col2 =st.columns(2)
        col1.selectbox("Select Month:",months,key="month")
        col2.selectbox("Select Year:",years,key="year")

        "---"
        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:",min_value=0,format="%i",step=10,key=income)
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}",min_value=0,format="%i",step=10,key=expense)
        with st.expander("Comment"):
            comment=st.text_area("",placeholder="Enter a comment here...")

            "___"
            submitted=st.form_submit_button("Save Data")
            if submitted:
                period=str(st.session_state["year"])+"_"+str(st.session_state["month"])
                incomes={income: st.session_state[income] for income in incomes}
                expenses={expense: st.session_state[expense] for expense in expenses}

                st.write(f"incomes:{incomes}")
                st.write(f"expenses:{expenses}") 
                st.success("Data saved!")



    #------DATA VISUALISATION
    st.header("Data Visualisation")
    with st.form("saved_periods"):
        period=st.selectbox("Select Period",["2023_March"])
        submitted=st.form_submit_button("Plot period")
        if submitted:
            comment="Some comment"
            incomes={'Salary':1500,'Blog':50,'Other Income':10}
            expenses={'Rent':600,'Utilites':200,'Groceries':300,'Car':100,'Other Expenses':50,'Saving':20}




            #metrics
            total_income=sum(incomes.values())
            total_expense=sum(expenses.values())
            remaining_budget=total_income-total_expense
            col1,col2,col3 = st.columns(3)
            col1.metric("Total Income",f"{total_income} {currency}")
            col2.metric("Total Expense",f"{total_expense}{currency}")
            col3.metric("Remaining Budget",f"{remaining_budget}{currency}")
            st.text(f"Comment:{comment}")


            #Create sankey chart
            label =list(incomes.keys())+["Total Income"] + list(expenses.keys())
            source=list(range(len(incomes)))+[len(incomes)]*len(expenses)
            target=[len(incomes)]*len(incomes)+[label.index(expense) for expense in expenses.keys()]
            value = list(incomes.values())+list(expenses.values())

            #data to dict, dict to sankey

            link = dict(source=source,target=target,value=value)
            node=dict(label=label,pad=20,thickness=30,color="#E694FF")
            data = go.Sankey(link=link,node=node)

            #plot it

            fig=go.Figure(data)
            fig.update_layout(margin=dict(l=0,r=0,t=5,b=5))
            st.plotly_chart(fig,use_container_width=True)










                                                         





