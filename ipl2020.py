import streamlit as st
import pandas as pd
import numpy as np
from sodapy import Socrata
import pydeck as pdk
import plotly.express as px
import requests
# from IPython.display import Image


with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

@st.cache(persist=True)
def giphy_path():
    path = "https://media.giphy.com/media/rS9tqucvXWwuY/giphy.gif"
    return path

path = giphy_path()

points_table_data_url = 'https://www.iplt20.com/points-table/2020'
# most_run_data_url = 'https://www.iplt20.com/stats/2020/most-runs'
html = requests.get(points_table_data_url).content
df_list_points_table = pd.read_html(html)
df_points_table = df_list_points_table[-1]
# print(df)
# df = pd.DataFrame(df)


# st.title("IPL 2020 Dashboard")
st.markdown("<h1 style='text-align: center; color: #9C021B;'><strong>🏏 <u>IPL 2020 Dashboard</u> 🏏</strong></h1>", unsafe_allow_html=True)
st.markdown("_________________________________________________________________________________")
# st.markdown("<h4 style='text-align: center; color: #9C021B;'><hr></h4>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: #E07811;'>You can check latest Status of IPL 2020 along with  stats of top Players</h4>", unsafe_allow_html=True)

# st.markdown("You can check latest Status of **IPL 2020** along with  stats of top Players 🏏")
st.markdown("&nbsp")
# st.markdown("&nbsp")

@st.cache(persist=True)
def load_data_point_table():
    data = pd.DataFrame(df_points_table)
    data.rename(columns={'Unnamed: 0': 'Position', 'Pld': 'Match Played', 'Pts': 'Points', 'Form':'Status of Past Matches'}, inplace=True)
    data = data.replace(np.nan, 'Not Played yet')
    return data


data_point_table = load_data_point_table()
# st.header("Points Table of IPL 2020")
st.markdown("<h2 style='text-align: center; color: blue;'><strong><u>Points Table of IPL 2020</u></strong></h2>", unsafe_allow_html=True)

st.write(data_point_table)
st.markdown("_________________________________________________________________________________")


# Batting & Bowling stats of all team
batting_stats_data_url = 'https://www.iplt20.com/stats/2020/most-runs'
# most_run_data_url = 'https://www.iplt20.com/stats/2020/most-runs'
html = requests.get(batting_stats_data_url).content
df_list_batting_stat = pd.read_html(html)
df_batting_stat = df_list_batting_stat[-1]
# print(df)


# st.markdown("&nbsp")
# st.markdown("&nbsp")
# st.header("Check Top Performers of Ongoing IPL Season")
st.markdown("<h2 style='text-align: center; color: green;'><strong><u>Check Top Performers of Ongoing IPL Season</u></strong></h2>", unsafe_allow_html=True)

select_bat_bowl = st.selectbox('Which stats you want to check?', ['--Select--', 'Batting stats', 'Bowling stats'])

if select_bat_bowl == 'Batting stats':

    @st.cache(persist=True)
    def load_data_batting_table():
        data = pd.DataFrame(df_batting_stat)
        data.rename(columns={'POS':'Position.',	'PLAYER': 'Player',	'Mat': 'Matches','Inns': 'Innings',	'NO':'Not Outs','HS': 'Highest Score',
        	                           'Avg': 'Average',	'BF': 'Ball Faced',	'SR': 'Strike Rate'	}, inplace=True)
        # data = data.replace(np.nan, 'Not Played yet')
        return data

    data_batting_stats = load_data_batting_table()

    if st.checkbox("Show Top 20 Batsman List (in terms of Total Runs Scored)", False):
        # st.header("Batting Stats of top Players")
        st.markdown("<h3 style='text-align: center; color: #4BC401;'><strong>Batting Stats of top Players</strong></h3>", unsafe_allow_html=True)

        st.write(data_batting_stats.head(20))
        st.markdown("_________________________________________________________________________________")

    # st.subheader("Check Top 3 Best Batsman in Selective categories")
    st.markdown("<h3 style='text-align: center; color: orangered;'><strong>Check Top 3 Best Batsman in Selective categories</strong></h3>", unsafe_allow_html=True)

    select_category = st.selectbox('Choose the Performance category', ['--Select--', 'Top Run Scorer', 'Highest Strike Rate', 'Best Average'])

    if select_category == 'Top Run Scorer':
        df_bat_total_score = data_batting_stats.sort_values(by=['Runs'], ascending=False).head(3)
        x = np.arange(1, 4)
        df_bat_total_score['Position'] = x

        data_batting_stats_new = df_bat_total_score[['Position', 'Player', 'Runs']].head(3)

        fig = px.bar(data_batting_stats_new, x='Player', y='Runs',text='Runs', hover_data=['Position','Player', 'Runs'], color='Player')
        fig.update_traces(texttemplate='%{text:.s}', textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        fig.update_layout(xaxis_title="Batsman",
                            yaxis_title="Total Runs Scored",
                            legend_title="Players",
                            font=dict(
                                family="Arial",
                                size=16,
                                color="RebeccaPurple"
                            ))

        fig.update_layout(title={'text': "Top 3 Most run scorer Batsman",
                                    'y':0.95,
                                    'x':0.43,
                                    'xanchor': 'center',
                                    'yanchor': 'top'})

        st.write(fig)
        st.markdown("_________________________________________________________________________________")

    elif select_category == 'Highest Strike Rate':
        df_bat_sr = data_batting_stats.sort_values(by=['Strike Rate'], ascending=False).head(3)
        x = np.arange(1, 4)
        df_bat_sr['Position'] = x
        data_batting_stats_sr = df_bat_sr[['Position', 'Player', 'Strike Rate']].head(3)

        fig2 = px.bar(data_batting_stats_sr, x='Player', y='Strike Rate',text='Strike Rate', hover_data=['Position','Player', 'Strike Rate'], color='Player')
        fig2.update_traces(texttemplate='%{text:.4s}', textposition='inside')
        fig2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        fig2.update_layout(xaxis_title="Batsman",
                            yaxis_title="Strike Rate",
                            legend_title="Players",
                            font=dict(
                                family="Arial",
                                size=16,
                                color="RebeccaPurple"
                            ))

        fig2.update_layout(title={'text': "Top 3 Batsman with Highest Strike Rate)",
                                    'y':0.95,
                                    'x':0.43,
                                    'xanchor': 'center',
                                    'yanchor': 'top'})

        st.write(fig2)
        st.markdown("🤔💡 * **Batting Strike rate** is measure of runs per ball. It is calculated in **%** *")
        st.markdown("_________________________________________________________________________________")

    elif select_category == 'Best Average':
        best_avg_data_url = 'https://www.iplt20.com/stats/2020/best-batting-average'
        # most_run_data_url = 'https://www.iplt20.com/stats/2020/most-runs'
        html = requests.get(best_avg_data_url).content
        df_list_avg = pd.read_html(html)
        df_batting_stat_best_avg = df_list_avg[-1]

        @st.cache(persist=True)
        def load_data_batting_table():
            data = pd.DataFrame(df_batting_stat_best_avg)
            data.rename(columns={'PLAYER':'Player', 'Avg': 'Average'}, inplace=True)
            # data = data.replace(np.nan, 'Not Played yet')
            return data

        data_best_avg_stats = load_data_batting_table()


        df_bat_bestavg = data_best_avg_stats.sort_values(by=['Average'], ascending=False).head(3)
        x = np.arange(1, 4)
        df_bat_bestavg['Position'] = x
        data_batting_stats_bestavg = df_bat_bestavg[['Position', 'Player', 'Average']].head(3)

        fig2 = px.bar(data_batting_stats_bestavg, x='Player', y='Average',text='Average', hover_data=['Position','Player', 'Average'], color='Player')
        fig2.update_traces(texttemplate='%{text:.4s}', textposition='inside')
        fig2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        fig2.update_layout(xaxis_title="Batsman",
                            yaxis_title="Best Average",
                            legend_title="Players",
                            font=dict(
                                family="Arial",
                                size=16,
                                color="RebeccaPurple"
                            ))

        fig2.update_layout(title={'text': "Top 3 Batsman with Best Average",
                                    'y':0.95,
                                    'x':0.42,
                                    'xanchor': 'center',
                                    'yanchor': 'top'})

        st.write(fig2)
        st.markdown("🤔💡 * **Batting average** is the **total number of runs** a batsman have scored divided by the **number of times** they have been out*")
        st.markdown("_________________________________________________________________________________")

##############################################################################################################################
#####################          Bowling

bowling_stats_data_url = 'https://www.iplt20.com/stats/2020/most-wickets'
# most_run_data_url = 'https://www.iplt20.com/stats/2020/most-runs'
html = requests.get(bowling_stats_data_url).content
df_list_bowling_stat = pd.read_html(html)
df_bowling_stat = df_list_bowling_stat[-1]


if select_bat_bowl == 'Bowling stats':

    @st.cache(persist=True)
    def load_data_bowling_table():
        data = pd.DataFrame(df_bowling_stat)
        data.rename(columns={'POS':'Position.',	'PLAYER': 'Player',	'Mat': 'Matches','Inns': 'Innings',	'Ov':'Overs','Wkts': 'Wickets taken',
        	                           'BBI': 'Best Bowling in a Inns',	'Avg': 'Average',	'Econ': 'Economy Rate', 'SR': 'Strike Rate'	}, inplace=True)
        # data = data.replace(np.nan, 'Not Played yet')
        return data

    data_bowling_stats = load_data_bowling_table()

    if st.checkbox("Show Top 20 Bowlers List (in terms of Total number of wickets taken)", False):
        # st.header("Bowling Stats of top Players")
        st.markdown("<h3 style='text-align: center; color: #4BC401;'><strong>Bowling Stats of top Players</strong></h3>", unsafe_allow_html=True)

        st.write(data_bowling_stats.head(20))
        st.markdown("_________________________________________________________________________________")
    # st.subheader("Check Top 3 Best Bowlers in Selective categories")
    st.markdown("<h3 style='text-align: center; color: purple;'><strong>Check Top 3 Best Bowlers in Selective categories</strong></h3>", unsafe_allow_html=True)

    select_category = st.selectbox('Choose the Performance category', ['--Select--', 'Top Wicket Taker', 'Best Economy Rate', 'Best Bowling Average'])

######################################### !st category
    if select_category == 'Top Wicket Taker':
        df_bowl_top_wicket = data_bowling_stats.sort_values(by=['Wickets taken'], ascending=False).head(3)
        x = np.arange(1, 4)
        df_bowl_top_wicket['Position'] = x

        data_bowl_stats_top_wkt = df_bowl_top_wicket[['Position', 'Player', 'Wickets taken']].head(3)

        fig = px.bar(data_bowl_stats_top_wkt, x='Player', y='Wickets taken',text='Wickets taken', hover_data=['Position','Player', 'Wickets taken'], color='Player')
        fig.update_traces(texttemplate='%{text:.s}', textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

        fig.update_layout(xaxis_title="Bowlers",
                            yaxis_title="Wickets taken so far",
                            legend_title="Players",
                            font=dict(
                                family="Arial",
                                size=16,
                                color="RebeccaPurple"
                            ))

        fig.update_layout(title={'text': "Top 3 Most Wicket taker",
                                    'y':0.95,
                                    'x':0.42,
                                    'xanchor': 'center',
                                    'yanchor': 'top'})

        st.write(fig)
        st.markdown("_________________________________________________________________________________")

    elif select_category == 'Best Economy Rate':
            df_bowl_best_er = data_bowling_stats.sort_values(by=['Economy Rate'], ascending=True).head(3)
            x = np.arange(1, 4)
            df_bowl_best_er['Position'] = x

            data_bowl_stats_best_er = df_bowl_best_er[['Position', 'Player', 'Economy Rate']].head(3)

            fig = px.bar(data_bowl_stats_best_er, x='Player', y='Economy Rate', text='Economy Rate', hover_data=['Position','Player', 'Economy Rate'], color='Player')
            fig.update_traces(texttemplate='%{text:.4s}', textposition='inside')
            fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

            fig.update_layout(xaxis_title="Bowlers",
                                yaxis_title="Economy Rate",
                                legend_title="Players",
                                font=dict(
                                    family="Arial",
                                    size=16,
                                    color="RebeccaPurple"
                                ))

            fig.update_layout(title={'text': "Top 3 Bowlers with Best Economy rate",
                                        'y':0.95,
                                        'x':0.40,
                                        'xanchor': 'center',
                                        'yanchor': 'top'})

            st.write(fig)
            st.markdown("🤔💡 * **Economy rate** is the number of runs a bowler have conceded per over bowled. The **lower** the economy rate is, the **better** the bowler is performing.*")
            st.markdown("_________________________________________________________________________________")


    elif select_category == 'Best Bowling Average':
            data_bowling_stats = data_bowling_stats[data_bowling_stats.Average != '-']
            df_bowl_best_avg = data_bowling_stats.sort_values(by=['Average'], ascending=True).head(3)
            x = np.arange(1, 4)
            df_bowl_best_avg['Position'] = x

            data_bowl_stats_best_avg = df_bowl_best_avg[['Position', 'Player', 'Average']].head(3)

            fig = px.bar(data_bowl_stats_best_avg, x='Player', y='Average',text='Average', hover_data=['Position','Player', 'Average'], color='Player', width=750)

            fig.update_traces(texttemplate='%{text:.4s}', textposition='inside')
            fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

            fig.update_layout(xaxis_title="Bowlers",
                                yaxis_title="Average",
                                legend_title="Players",
                                font=dict(
                                    family="Arial",
                                    size=16,
                                    color="RebeccaPurple"
                                ))

            fig.update_layout(title={'text': "Top 3 Bowlers with Best Bowling Average",
                                        'y':0.95,
                                        'x':0.40,
                                        'xanchor': 'center',
                                        'yanchor': 'top'})

            st.write(fig)
            st.markdown("🤔💡 * **Bowling average** is the number of runs a bowler have conceded per wicket taken. The **lower** the bowling average is, the **better** the bowler is performing*")
            st.markdown("_________________________________________________________________________________")


#########################################################################################################################################
#########################################################################################################################################















# st.sidebar.title("Schedule of IPL 2020")
st.sidebar.markdown("<h1 style='text-align: center; color: #F34600;'><u><strong>Schedule of IPL 2020</strong></u></h1>", unsafe_allow_html=True)

# st.sidebar.markdown("You can check the scheduled matches of IPL 2020, along with various other details like timing, Venue etc.")
st.sidebar.markdown("<h4 style='text-align: center; '>You can check all the scheduled matches of IPL 2020, along with various other details like timing, Venue etc.</h4>", unsafe_allow_html=True)

st.sidebar.markdown("_________________________________________________________________________________")


# st.sidebar.markdown("&nbsp")
# st.sidebar.markdown("&nbsp")
# st.sidebar.subheader("Want to check all scheduled Matches?")
st.sidebar.markdown("<h2 style='text-align: center; color: #BD08D3;'><strong>Want to check all scheduled Matches?</strong></h2>", unsafe_allow_html=True)


if st.sidebar.checkbox("Show IPL 2020 scheduled matches", False):
    st.markdown("&nbsp")
    # st.markdown("&nbsp")
    # st.header("IPL 2020 Scheduled Matches")
    st.markdown("<h2 style='text-align: center; color: #BD08D3;'><strong><u>All Scheduled matches of IPL 2020</u></strong></h2>", unsafe_allow_html=True)

    # st.header("Bowling Stats of top Players")
    all_match = st.slider("Adjust the slider if you want to check more Scheduled Matches?", 20, 60)
    st.markdown("<h4 style='text-align: center;'><i>You can view in fullscreen for better visibility of Schedule</i></h4>", unsafe_allow_html=True)

    # st.markdown("You can expand the view for better visibility of Time table")
    image = pd.read_csv('ipl_schedule.csv')
    # st.image(image, use_column_width=True)
    imag= image[['Match No', 'Match Center', 'Date', 'Day', 'Time India (IST)', 'Venuue']]
    # imag = imag.style.hide_index()
    # imag.set_index('column', inplace=True)
    st.write(image.head(all_match))
    st.markdown("_________________________________________________________________________________")


    # st.table(imag.assign(hack='').set_index('hack').head(all_match))

# st.sidebar.markdown("&nbsp")
# st.sidebar.markdown("&nbsp")
# st.sidebar.subheader("Want to check scheduled Matches of your favourite team?")
st.sidebar.markdown("_________________________________________________________________________________")
st.sidebar.markdown("<h2 style='text-align: center; color: #5A2553;'><strong>Want to check scheduled Matches of your favourite team?</strong></h2>", unsafe_allow_html=True)


favourite_team = st.sidebar.selectbox("Which's your favourite team?", ['--Select--', 'Chennai Super Kings (CSK)', 'Mumbai Indians (MI)', 'Royal Challengers Benglore (RCB)', 'Sunrisers Hyderabad (SRH)', 'Delhi Capitals (DC)', 'Kings Eleven Punjab (KXIP)', 'Rajasthan Royals (RR)', 'Kolkata knight Riders (KKR)'])



if favourite_team == 'Chennai Super Kings (CSK)':
    # @st.cache(persist=True)
    csk = pd.read_csv('csk_schedule.csv')
    # st.image(image, use_column_width=True)
    csk= csk[['Match No', 'Match Center', 'Date', 'Day', 'Time India (IST)', 'Venuue']]
    # imag = imag.style.hide_index()
    # imag.set_index('column', inplace=True)
    # st.write(csk)
    st.markdown("&nbsp")
    # st.markdown("&nbsp")
    # st.header("Chennai Super Kings full Schedule of Matches")
    st.markdown("<h2 style='text-align: center; color: #DBB000;'><strong><u>Chennai Super Kings full Schedule of Matches</strong></h2>", unsafe_allow_html=True)

    st.table(csk.assign(hack='').set_index('hack'))
    # st.markdown("_________________________*****___________________________")
    st.markdown("<h2 style='text-align: center; color: #DBB000;'><strong><u>_____________________*****_____________________</strong></h2>", unsafe_allow_html=True)



#
elif favourite_team == 'Mumbai Indians (MI)':
    mi = pd.read_csv('mi_schedule.csv')
    mi= mi[['Match No', 'Match Center', 'Date', 'Day', 'Time India (IST)', 'Venuue']]
    st.markdown("&nbsp")
    # st.markdown("&nbsp")
    # st.header("Mumbai Indians full Schedule of Matches")
    st.markdown("<h2 style='text-align: center; color: #006EC9;'><strong><u>Mumbai Indians full Schedule of Matches</u></strong></h2>", unsafe_allow_html=True)

    st.table(mi.assign(hack='').set_index('hack'))
    st.markdown("<h2 style='text-align: center; color: #006EC9;'><strong><u>_____________________*****_____________________</strong></h2>", unsafe_allow_html=True)


elif favourite_team == 'Royal Challengers Benglore (RCB)':
    rcb = pd.read_csv('rcb_schedule.csv')
    rcb= rcb[['Match No', 'Match Center', 'Date', 'Day', 'Time India (IST)', 'Venuue']]
    st.markdown("&nbsp")
    # st.markdown("&nbsp")
    # st.header("Royal Challengers Benglore full Schedule of Matches")
    st.markdown("<h2 style='text-align: center; color: #F30922;'><strong><u>Royal Challengers Benglore full Schedule of Matches</u></strong></h2>", unsafe_allow_html=True)

    st.table(rcb.assign(hack='').set_index('hack'))
    st.markdown("<h2 style='text-align: center; color: #F30922;'><strong><u>_____________________*****_____________________</strong></h2>", unsafe_allow_html=True)


elif favourite_team == 'Sunrisers Hyderabad (SRH)':
    srh = pd.read_csv('srh_schedule.csv')
    srh= srh[['Match No', 'Match Center', 'Date', 'Day', 'Time India (IST)', 'Venuue']]
    st.markdown("&nbsp")
    # st.markdown("&nbsp")
    # st.header("Sunrisers Hyderabad full Schedule of Matches")
    st.markdown("<h2 style='text-align: center; color: #F32C09;'><strong><u>Sunrisers Hyderabad full Schedule of Matches</u></strong></h2>", unsafe_allow_html=True)
    st.table(srh.assign(hack='').set_index('hack'))
    st.markdown("<h2 style='text-align: center; color: #F32C09;'><strong><u>_____________________*****_____________________</strong></h2>", unsafe_allow_html=True)



elif favourite_team == 'Delhi Capitals (DC)':
    dc = pd.read_csv('dc_schedule.csv')
    dc= dc[['Match No', 'Match Center', 'Date', 'Day', 'Time India (IST)', 'Venuue']]
    st.markdown("&nbsp")
    # st.markdown("&nbsp")
    # st.header("Delhi Capitals full Schedule of Matches")
    st.markdown("<h2 style='text-align: center; color: #4403E3;'><strong><u>Delhi Capitals full Schedule of Matches</u></strong></h2>", unsafe_allow_html=True)
    st.table(dc.assign(hack='').set_index('hack'))
    st.markdown("<h2 style='text-align: center; color: #4403E3;'><strong><u>_____________________*****_____________________</strong></h2>", unsafe_allow_html=True)


elif favourite_team == 'Kings Eleven Punjab (KXIP)':
    punjab = pd.read_csv('punjab_schedule.csv')
    punjab= punjab[['Match No', 'Match Center', 'Date', 'Day', 'Time India (IST)', 'Venuue']]
    st.markdown("&nbsp")
    # st.markdown("&nbsp")
    # st.header("RKings Eleven Punjab full Schedule of Matches")
    st.markdown("<h2 style='text-align: center; color: #E10000;'><strong><u>Kings Eleven Punjab full Schedule of Matches</u></strong></h2>", unsafe_allow_html=True)
    st.table(punjab.assign(hack='').set_index('hack'))
    st.markdown("<h2 style='text-align: center; color: #E10000;'><strong><u>_____________________*****_____________________</strong></h2>", unsafe_allow_html=True)


elif favourite_team == 'Rajasthan Royals (RR)':
    rr = pd.read_csv('rajasthan_schedule.csv')
    rr= rr[['Match No', 'Match Center', 'Date', 'Day', 'Time India (IST)', 'Venuue']]
    st.markdown("&nbsp")
    # st.markdown("&nbsp")
    # st.header("Rajasthan Royals full Schedule of Matches")
    st.markdown("<h2 style='text-align: center; color: #F519AC;'><strong><u>Rajasthan Royals full Schedule of Matches</u></strong></h2>", unsafe_allow_html=True)
    st.table(rr.assign(hack='').set_index('hack'))
    st.markdown("<h2 style='text-align: center; color: #F519AC;'><strong><u>_____________________*****_____________________</strong></h2>", unsafe_allow_html=True)


elif favourite_team == 'Kolkata knight Riders (KKR)':
    kkr = pd.read_csv('kkr_schedule.csv')
    kkr= kkr[['Match No', 'Match Center', 'Date', 'Day', 'Time India (IST)', 'Venuue']]
    st.markdown("&nbsp")
    # st.markdown("&nbsp")
    # st.header("Kolkata knight Riders full Schedule of Matches")
    st.markdown("<h2 style='text-align: center; color: #3328B3;'><strong><u>Kolkata knight Riders full Schedule of Matches</u></strong></h2>", unsafe_allow_html=True)
    st.table(kkr.assign(hack='').set_index('hack'))
    st.markdown("<h2 style='text-align: center; color: #3328B3;'><strong><u>_____________________*****_____________________</strong></h2>", unsafe_allow_html=True)



# with open("/home/dheeraj/my_projects/my_project_env/practice/IPL2020_Dashnoard/style.css") as f:
#     st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
#
# path = "https://media.giphy.com/media/rS9tqucvXWwuY/giphy.gif"
st.markdown("&nbsp")
st.image(path, width = 300)


# st.write("bye world")
# bye = '/home/dheeraj/my_projects/my_project_env/practice/IPL2020_Dashnoard/bye.png'
# st.image(bye, width=150)

# st.markdown("<img src='/home/dheeraj/my_projects/my_project_env/practice/IPL2020_Dashnoard/bye.png' >", unsafe_allow_html=True)

# <iframe src="https://giphy.com/embed/rS9tqucvXWwuY" width="480" height="271" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/stickers/bye-rS9tqucvXWwuY">via GIPHY</a></p>
# <img src="/home/dheeraj/my_projects/my_project_env/practice/IPL2020_Dashnoard/bye.png" alt="Italian Trulli">
# st.markdown("![Alt Text](https://media.giphy.com/media/rS9tqucvXWwuY/giphy.gif)")
