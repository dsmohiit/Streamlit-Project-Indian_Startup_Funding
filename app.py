# Plan of Action: "https://docs.google.com/document/d/1zk4751zmG2b4XnYGW06tu0MWyr2PgLlMaSci7eUVL2M/edit"

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout= "wide", page_title= "Startup Analysis")
df = pd.read_csv("startup_cleaned.csv")
df["date"] = pd.to_datetime(df["date"], errors= "coerce")
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year


def load_overall_analysis():
    st.title("Overall Analysis")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Total investment
        total = round(df["amount"].sum())
        st.metric("Total Investment", str(total) + " Cr")

    with col2:
        # Maximum Funding
        max_investment = df.groupby("startup")["amount"].max().sort_values(ascending= False).head(1).values[0]
        st.metric("Maximum Investment", str(max_investment) + " Cr")

    with col3:
        # Avg funding
        avg_funding = round(  df.groupby("startup")["amount"].sum().mean())
        st.metric("Average Funding", str(avg_funding) + " Cr")

    with col4:
        # Total funded startups
        funded_startup = df["startup"].nunique()
        st.metric("Total Funded Startups", str(funded_startup) + " Cr ")

    col1, col2 = st.columns(2)
    with col1:
        # MoM Investment
        st.header("MoM Investment")
        selected_option = st.selectbox("Select Type", ["Total", "Count"])
        if selected_option == "Total":
            temp_df = df.groupby(["year", "month"])["amount"].sum().reset_index()
        else:
            temp_df = df.groupby(["year", "month"])["amount"].count().reset_index()

        temp_df["x-axis"] = temp_df["year"].astype("str") + "-" + temp_df["month"].astype("str")

        fig5, ax5 = plt.subplots()
        ax5.plot(temp_df["x-axis"], temp_df["amount"])

        st.pyplot(fig5)

    col1, col2 = st.columns(2)
    with col1:
        # Sector analysis(Top sector)
        st.header("Top Sector/Investment Vertical")
        select_option = st.selectbox("Select One", ["Count", "Total"])
        if select_option == "Count":
            sector = df.groupby("vertical")["investor"].count()

            fig6, ax6 = plt.subplots()
            ax6.pie(sector, labels=sector.index, autopct="%0.01f%%")

            st.pyplot(fig6)

        else:
            sector = df.groupby("vertical")["amount"].sum()

            fig7, ax7 = plt.Subplot()
            ax7.pie(sector, labels= sector.index, autopct="%0.01f%%")

            st.pyplot(fig7)

    with col2:
        # Round of funding
        st.header("Round of Funding")
        round_funding = df.groupby("round")["investor"].count()

        fig8, ax8 = plt.subplots()
        ax8.pie(round_funding, labels=round_funding.index, autopct="%0.01f%%")

        st.pyplot(fig8)

    col1, col2 = st.columns(2)
    with col1:
        # City of funding
        st.header("City of Funding")
        city_funding = round(df.groupby("city")["amount"].sum())

        fig9, ax9 = plt.subplots()
        ax9.pie(city_funding, labels= city_funding.index, autopct="%0.01f%%")

        st.pyplot(fig9)

    col1, col2 = st.columns(2)
    with col1:
        # Top Startup
        st.header("Top Startups")
        top_startup = df.groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        st.dataframe(top_startup)

    with col2:
        # Top Investor
        st.header("Top Investor")
        top_investor = round(df.groupby("investor")["amount"].sum().sort_values(ascending=False).head(5))
        st.dataframe(top_investor)


def load_investor_details(investor):
    st.title(investor)

    # loading last 5 investment of investor
    last_5_df = df[df["investor"].str.contains(investor)].head()[
        ["date", "startup", "vertical", "city", "round", "amount"]]
    st.subheader("Most Recent Investment: ")
    st.dataframe(last_5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investment
        biggest_investment = df[df["investor"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(
            ascending=False).head(3)

        st.subheader("Biggest Investment: ")
        fig, ax = plt.subplots()
        ax.bar(biggest_investment.index, biggest_investment.values)

        st.pyplot(fig)
    with col2:
        # investment vertical
        investment_vertical = df[df["investor"].str.contains(investor)].groupby("vertical")["amount"].sum()

        st.subheader("Investment Verticals: ")
        fig1, ax1 = plt.subplots()
        ax1.pie(investment_vertical, labels= investment_vertical.index, autopct= "%0.01f%%")

        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        # Stage of investment
        investment_stage = df[df["investor"].str.contains(investor)].groupby("round")["amount"].sum()

        st.subheader("Investment Stage: ")
        fig2, ax2 = plt.subplots()
        ax2.pie(investment_stage, labels=investment_stage.index, autopct="%0.01f%%")

        st.pyplot(fig2)

    with col4:
        # City of investment
        investment_city = df[df["investor"].str.contains(investor)].groupby("city")["amount"].sum()

        st.subheader("Investment City: ")
        fig3, ax3 = plt.subplots()
        ax3.pie(investment_city, labels=investment_city.index, autopct="%0.01f%%")

        st.pyplot(fig3)

    col5, col6 = st.columns(2)
    with col5:
        # YoY investment
        yoy_investment = df[df["investor"].str.contains(investor)].groupby("year")["amount"].sum()

        st.subheader("YoY Investment: ")
        fig4, ax4 = plt.subplots()
        ax4.plot(yoy_investment.index, yoy_investment.values)

        st.pyplot(fig4)


st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox("Select One", ["Overall Analysis", "Startup Analysis", "Investor Analysis"])

if option == "Overall Analysis":
        load_overall_analysis()

elif option == "Startup Analysis":
    st.sidebar.selectbox("Select Startup", sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button("Find Startup Details")
    st.title("Startup Analysis")
else:
    selected_investor = st.sidebar.selectbox("Select Investor", sorted(set(df["investor"].str.split(",").sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)
