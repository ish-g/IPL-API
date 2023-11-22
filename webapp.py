import streamlit as st
import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt


def show_teams_name():
    data1 = requests.get("https://iplapiishg.pythonanywhere.com/").json()
    l1 = list(data1['_All Teams Name']['team_names'].values())
    return l1


def teamvteam(response2):
    data2 = response2.get('teamvteam', {})
    columns = st.columns(len(data2))
    for x2, y2 in enumerate(data2):
        columns[x2].metric(y2, data2[y2], delta=None)
    st.divider()


def team_record_section(response3):
    overall = response3.get('Team-Record', {}).get('Overall', {})
    st.markdown("<p style='font-size: 50px; color: red;'>Overall</p>", unsafe_allow_html=True)
    columns = st.columns(len(overall))
    for j3, i3 in enumerate(overall):
        columns[j3].metric(i3, overall[i3], delta=None)
    st.divider()
    against = response3.get('Team-Record', {}).get('Against', {})
    st.markdown("<p style='font-size: 50px; color: yellow;'>Against</p>", unsafe_allow_html=True)
    for i in against:
        against1 = against[i]
        st.subheader(i)
        columns = st.columns(len(against1))
        st.divider()
        for j4, k4 in enumerate(against1):
            columns[j4 % 4].metric(k4, against1[k4], delta=None)


def win_pct(response4):
    against = response4.get('Team-Record', {}).get('Against', {})
    x = []
    y = []
    for j, i in enumerate(against):
        x.append(i)
        try:
            y.append(round(against[i]['Won'] / against[i]['MatchesPlayed'] * 100))
        except:
            y.append(0)
    data = pd.DataFrame(data=zip(x, y), columns=["Teams Name", "Percentage to win"])
    with st.expander("Click to expand dataframe"):
        st.dataframe(data)
    st.bar_chart(data=data, x="Teams Name", y="Percentage to win", color="#ffaa00", use_container_width=True)


def batsman_record(response6):
    response6 = response6.get("Batsman Record", {})
    four_counts = np.array(response6.get("Total Four", {}))
    six_counts = np.array(response6.get("Total Six", {}))
    col1, col2 = st.columns(2)
    with col1:
        st.write("Four on over balls")
        fig1, axe1 = plt.subplots()
        axe1.pie(four_counts, labels=np.arange(1, len(four_counts)+1), autopct="%0.1f%%")
        st.pyplot(fig1)
    with col2:
        st.write("Six on over balls")
        fig2, axe2 = plt.subplots()
        axe2.pie(six_counts, labels=np.arange(1, len(six_counts)+1), autopct="%0.1f%%")
        st.pyplot(fig2)


def main():
    st.title("Welcome to IPL Stats OceanApp")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Teams Name", "Team vs Team Record", "Team Record", "Win %", "Player's(4/6)"])

    with tab1:
        dict1 = {'IPL team names': show_teams_name()}
        st.table(dict1)

    with tab2:
        i = st.selectbox("Select a 1st IPL team here", show_teams_name())
        l2 = show_teams_name()
        l2.remove(i)
        j = st.selectbox("Select a 2nd IPL team here", l2)
        enter1 = st.button("Enter", key="4554_1")
        if enter1:
            response = requests.get(f"https://iplapiishg.pythonanywhere.com/api/teamvteam?team1={i}&team2={j}").json()
            return teamvteam(response)

    with tab3:
        i3 = st.selectbox("Select any Team here", show_teams_name())
        enter = st.button("Enter", key="4554_3")
        if enter:
            response3 = requests.get(f"https://iplapiishg.pythonanywhere.com/api/team-record?team={i3}").json()
            return team_record_section(response3)

    with tab4:
        i4 = st.selectbox("Select a IPL team here", show_teams_name())
        enter = st.button("Enter", key="4554_4")
        if enter:
            response4 = requests.get(f"https://iplapiishg.pythonanywhere.com/api/team-record?team={i4}").json()
            return win_pct(response4)

    with tab5:
        response5 = requests.get(f"https://iplapiishg.pythonanywhere.com/api/batsman-names").json()
        l5 = response5.get("Batsman Names", {})
        i5 = st.selectbox("Select the Player name here", l5)
        enter = st.button("Enter", key='4554_5')
        if enter:
            response6 = requests.get(f"https://iplapiishg.pythonanywhere.com/api/batsman-record?batsman={i5}").json()
            batsman_record(response6)

st.set_option('deprecation.showfileUploaderEncoding', False)

if __name__ == "__main__":
    main()
