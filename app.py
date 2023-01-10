import streamlit as st
import Medal_census as ms
import preprocessing as ps
import pickle
import overall_analysis
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import countrywise_analysis
import plotly.figure_factory as ff
import Athelete_wise_analysis
from streamlit_option_menu import option_menu

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Olympic analysis", layout="wide")
st.markdown("<h1 style='text-align: center; color: Dark Grey;'>Olympics Data Analysis</h1>",unsafe_allow_html=True)

st.sidebar.image("https://cdn.britannica.com/44/190944-131-7D082864/Silhouette-hand-sport-torch-flag-rings-Olympic-February-3-2015.jpg")
st.sidebar.write("##")
with st.sidebar:
    season_radio = option_menu(
        menu_title = "Season",
        options = ['Summer Olympics','Winter Olympics'],
        icons = ['thermometer-sun','thermometer-snow'],
        menu_icon = 'thermometer',
        default_index = 0,
        orientation = 'horizontal',
        styles={
            "icon": {"font-size": "15px"},
            "nav-link": {"font-size": "15px"}
        }
    )

st.sidebar.write("##")
st.sidebar.image("https://stillmed.olympics.com/media/Images/B2B/Beyond-The-Games/CTA/Sustainability-CTA.jpg")

if season_radio == 'Summer Olympics':
    tab = option_menu(
        menu_title = None,
        options = ["About Olympics", "Leader Board", "Overall Analysis", "Country wise Analysis","Athelete wise Analysis", "Get in Touch with Me"],
        icons = ['cursor','table','clipboard-data','globe','bar-chart-line',"envelope-open"],
        default_index = 0,
        orientation = 'horizontal',
        styles={
            "icon": {"font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "centre"}
        }
    )

    if tab == "About Olympics":
        st.write("##")
        f = open('about.txt','r')
        data = f.readlines()
        st.write(data[0])
        st.write(" ")
        st.write(" ")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("1406765016013-opening-cermony.jpg")
        with col2:
            st.image("Screenshot.png")
        with col3:
            st.image("1518598865.jpg")
        st.write(" ")
        st.write(data[2])
        st.write(data[4])
        st.write(data[6])
        st.write(data[8])
        st.write(data[10])
        st.write(data[12])


    elif tab == "Leader Board":
        df = ps.s_initial_load()

        col1,col2 = st.columns(2)

        year = col1.selectbox(
            "Year",
            pickle.load(open("year.txt","rb"))
        )
        country = col2.selectbox(
            "Country",
            pickle.load(open("regions.txt","rb"))
        )
        # sport = st.sidebar.selectbox(
        #     "Sports",
        #     pickle.load(open("sports.txt","rb"))
        # )
        title,df = ms.medal_census(df,year,country)
        st.subheader(title)
        st.table(df)


    elif tab == "Overall Analysis":
        df = ps.s_initial_load()

        st.header("Overall Analysis")
        
        editions = df['Year'].unique().shape[0] - 1
        cities = df['City'].unique().shape [0]
        sports = df['Sport' ].unique().shape [0]
        events = df['Event'].unique() .shape [0]
        athletes = df['Name'].unique().shape [0]
        nations = df['region'].unique().shape [0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Editions</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{editions}</h1>""",unsafe_allow_html=True)

            st.subheader("")

            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Events</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{events}</h1>""",unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Hosts</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{cities}</h1>""",unsafe_allow_html=True)

            st.subheader("")

            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Athletes</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{athletes}</h1>""",unsafe_allow_html=True)

        
        with col3:
            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Sports</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{sports}</h1>""",unsafe_allow_html=True)

            st.subheader("")

            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Nations</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{nations}</h1>""",unsafe_allow_html=True)

        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.subheader("Participating countries over the years")
        plot_df = overall_analysis.over_time(df,'region')
        fig = px.line(plot_df, x = 'Edition', y = 'region')
        st.plotly_chart(fig)

        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.subheader("Events over the years")
        plot_df = overall_analysis.over_time(df,'Event')
        fig = px.line(plot_df, x = 'Edition', y = 'Event')
        st.plotly_chart(fig)

        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.subheader("Athletes over the years")
        plot_df = overall_analysis.over_time(df,'Name','Athletes')
        fig = px.line(plot_df, x = 'Edition', y = 'Athletes')
        st.plotly_chart(fig)

        st.write(' ')
        st.write(' ')
        st.subheader("No. of events over time")
        fig,ax = plt.subplots(figsize = (20,20))
        x = df.drop_duplicates (['Year', 'Sport', 'Event'])
        ax = sns.heatmap(x.pivot_table(index='Sport', columns= 'Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
        st.pyplot(fig)


        st.write(' ')
        st.write(' ')
        st.subheader("Most Decorated players")
        col1, col2,col3 = st.columns(3)

        sport_select = col2.selectbox(
            "Choose a sport for the following table",
            pickle.load(open("sports.txt","rb"))
        )

        st.table(overall_analysis.best_player(df,sport_select))


    elif tab == "Country wise Analysis":
        df = ps.s_initial_load()

        col1, col2, col3 = st.columns(3)
        country_select = col2.selectbox(
            "Choose a Country for Analysis",
            pickle.load(open("regions.txt","rb"))[1:],
            index = 191
        )

        st.subheader("Medals over the Years")
        temp_df = countrywise_analysis.countrywise_analysis(df,country_select)
        fig = px.line(temp_df, x = 'Year', y = 'Medal')
        st.plotly_chart(fig)

        st.subheader(country_select+"'s analysis over all sports")

        x = countrywise_analysis.countrywise_heatmap(df,country_select)
        fig,ax = plt.subplots(figsize = (20,20))
        ax = sns.heatmap(x.pivot_table(index='Sport', columns= 'Year', values='Medal', aggfunc='count').fillna(0).astype('int'), annot=True)
        st.pyplot(fig)

        st.write("")
        st.write("")
        st.subheader("Top 10 players from "+country_select)
        st.table(countrywise_analysis.best_player(df,country_select))

    elif tab == "Athelete wise Analysis":
        df = ps.s_initial_load()

        st.subheader("Distribution of age wrt Medals Won")
        x1,x2,x3,x4 = Athelete_wise_analysis.athelete_age(df)
        fig = ff.create_distplot([x1,x2,x3,x4],['Medalist Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug= False)
        fig.update_layout(autosize = False, width = 1000, height = 600)
        st.plotly_chart(fig)

        st.subheader("Age distribution wrt to different games(Gold Medal)")
        x,name = Athelete_wise_analysis.age_sports(df,'Gold')
        fig = ff.create_distplot(x,name,show_hist=False,show_rug= False)
        fig.update_layout(autosize = False, width = 1000, height = 600)
        st.plotly_chart(fig)

        st.subheader("Age distribution wrt to different games(Silver Medal)")
        x,name = Athelete_wise_analysis.age_sports(df,'Silver')
        fig = ff.create_distplot(x,name,show_hist=False,show_rug= False)
        fig.update_layout(autosize = False, width = 1000, height = 600)
        st.plotly_chart(fig)

        st.subheader("Age distribution wrt to different games(Bronze Medal)")
        x,name = Athelete_wise_analysis.age_sports(df,'Bronze')
        fig = ff.create_distplot(x,name,show_hist=False,show_rug= False)
        fig.update_layout(autosize = False, width = 1000, height = 600)
        st.plotly_chart(fig)

        col1, col2,col3 = st.columns(3)

        sport_select_awa = col2.selectbox(
            "Choose a sport for the following Plot",
            pickle.load(open("sports.txt","rb"))
        )

        st.subheader("Winnings on the basis of Height and Weight")
        fig = px.scatter(Athelete_wise_analysis.height_weight_scatter(df,sport_select_awa),x = "Weight",y='Height',color = 'Medal',symbol = 'Sex')
        st.plotly_chart(fig)

        st.subheader("Male vs Female Participation")
        fig = px.line(Athelete_wise_analysis.male_vs_female(df),x = 'Year', y = ['Male','Female'])
        st.plotly_chart(fig)

    elif tab == "Get in Touch with Me":
        contact_form = '''
        <form action="https://formsubmit.co/tokas.2sonu@gmail.com" method="POST">
            <input type="hidden" name="_autoresponse" value="Thank You for spending your valuable time on my website. I will contact you soon.">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_next" value="https://vivek-2567-olympic-games-data-analysis-app-zrn7gl.streamlit.app">
            <input type="text" name="name" id = 'input' placeholder = "Your Name" required>
            <input type="email" name="email" id = 'input' placeholder = "Your Email" required>
            <textarea name = 'message' id = 'input' placeholder = 'Your Message' required></textarea>
            <button onclick="document.getElementById('input').value = ''" type="submit">Send</button>
        </form>
        '''

        st.write("##")
        st.markdown(contact_form,unsafe_allow_html=True)
        local_css("style/style.css")



elif season_radio == 'Winter Olympics':

    tab = option_menu(
        menu_title = None,
        options = ["About Olympics", "Leader Board", "Overall Analysis", "Country wise Analysis","Athelete wise Analysis", "Get in Touch with Me"],
        icons = ['cursor','table','clipboard-data','globe','bar-chart-line',"envelope-open"],
        default_index = 0,
        orientation = 'horizontal',
        styles={
            "icon": {"font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "centre"}
        }
    )

    if tab == "About Olympics":
        f = open('about.txt','r')
        data = f.readlines()
        st.write(data[0])
        st.write(" ")
        st.write(" ")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("1406765016013-opening-cermony.jpg")
        with col2:
            st.image("Screenshot.png")
        with col3:
            st.image("1518598865.jpg")
        st.write(" ")
        st.write(data[2])
        st.write(data[4])
        st.write(data[6])
        st.write(data[8])
        st.write(data[10])
        st.write(data[12])

    elif tab == "Leader Board":
        df = ps.w_initial_load()

        col1,col2 = st.columns(2)

        year = col1.selectbox(
            "Year",
            pickle.load(open("w_year.txt","rb"))
        )
        country = col2.selectbox(
            "Country",
            pickle.load(open("w_regions.txt","rb"))
        )
        # sport = st.sidebar.selectbox(
        #     "Sports",
        #     pickle.load(open("sports.txt","rb"))
        # )
        title,df = ms.medal_census(df,year,country)
        st.subheader(title)
        st.table(df)


    elif tab == "Overall Analysis":
        df = ps.w_initial_load()

        st.header("Overall Analysis")
        
        editions = df['Year'].unique().shape[0]
        cities = df['City'].unique().shape [0]
        sports = df['Sport' ].unique().shape [0]
        events = df['Event'].unique() .shape [0]
        athletes = df['Name'].unique().shape [0]
        nations = df['region'].unique().shape [0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Editions</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{editions}</h1>""",unsafe_allow_html=True)

            st.subheader("")

            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Events</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{events}</h1>""",unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Hosts</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{cities}</h1>""",unsafe_allow_html=True)

            st.subheader("")

            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Athletes</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{athletes}</h1>""",unsafe_allow_html=True)

        
        with col3:
            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Sports</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{sports}</h1>""",unsafe_allow_html=True)

            st.subheader("")

            st.markdown("<h2 style='text-align: center; color: Dark Grey;'>Nations</h2>",unsafe_allow_html=True)
            st.markdown(f"""<h1 style='text-align: center; color: Dark Grey;'>{nations}</h1>""",unsafe_allow_html=True)

        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.subheader("Participating countries over the years")
        plot_df = overall_analysis.over_time(df,'region')
        fig = px.line(plot_df, x = 'Edition', y = 'region')
        st.plotly_chart(fig)

        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.subheader("Events over the years")
        plot_df = overall_analysis.over_time(df,'Event')
        fig = px.line(plot_df, x = 'Edition', y = 'Event')
        st.plotly_chart(fig)

        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.subheader("Athletes over the years")
        plot_df = overall_analysis.over_time(df,'Name','Athletes')
        fig = px.line(plot_df, x = 'Edition', y = 'Athletes')
        st.plotly_chart(fig)

        st.write(' ')
        st.write(' ')
        st.subheader("No. of events over time")
        fig,ax = plt.subplots(figsize = (20,20))
        x = df.drop_duplicates (['Year', 'Sport', 'Event'])
        ax = sns.heatmap(x.pivot_table(index='Sport', columns= 'Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
        st.pyplot(fig)


        st.write(' ')
        st.write(' ')
        st.subheader("Most Decorated players")
        col1, col2,col3 = st.columns(3)

        sport_select = col2.selectbox(
            "Choose a sport for the following table",
            pickle.load(open("w_sports.txt","rb"))
        )

        st.table(overall_analysis.best_player(df,sport_select))


    elif tab == "Country wise Analysis":
        df = ps.w_initial_load()

        col1, col2, col3 = st.columns(3)
        country_select = col2.selectbox(
            "Choose a Country for Analysis",
            pickle.load(open("w_regions.txt","rb"))[1:],
            index = 1
        )

        st.subheader("Medals over the Years")
        temp_df = countrywise_analysis.countrywise_analysis(df,country_select)
        fig = px.line(temp_df, x = 'Year', y = 'Medal')
        st.plotly_chart(fig)

        st.subheader(country_select+"'s analysis over all sports")

        x = countrywise_analysis.countrywise_heatmap(df,country_select)
        fig,ax = plt.subplots(figsize = (20,20))
        ax = sns.heatmap(x.pivot_table(index='Sport', columns= 'Year', values='Medal', aggfunc='count').fillna(0).astype('int'), annot=True)
        st.pyplot(fig)

        st.write("")
        st.write("")
        st.subheader("Top 10 players from "+country_select)
        st.table(countrywise_analysis.best_player(df,country_select))

    elif tab == "Athelete wise Analysis":
        df = ps.w_initial_load()

        st.subheader("Distribution of age wrt Medals Won")
        x1,x2,x3,x4 = Athelete_wise_analysis.athelete_age(df)
        fig = ff.create_distplot([x1,x2,x3,x4],['Medalist Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug= False)
        fig.update_layout(autosize = False, width = 1000, height = 600)
        st.plotly_chart(fig)

        st.subheader("Age distribution wrt to different games(Gold Medal)")
        x,name = Athelete_wise_analysis.w_age_sports(df,'Gold')
        fig = ff.create_distplot(x,name,show_hist=False,show_rug= False)
        fig.update_layout(autosize = False, width = 1000, height = 600)
        st.plotly_chart(fig)

        st.subheader("Age distribution wrt to different games(Silver Medal)")
        x,name = Athelete_wise_analysis.w_age_sports(df,'Silver')
        fig = ff.create_distplot(x,name,show_hist=False,show_rug= False)
        fig.update_layout(autosize = False, width = 1000, height = 600)
        st.plotly_chart(fig)

        st.subheader("Age distribution wrt to different games(Bronze Medal)")
        x,name = Athelete_wise_analysis.w_age_sports(df,'Bronze')
        fig = ff.create_distplot(x,name,show_hist=False,show_rug= False)
        fig.update_layout(autosize = False, width = 1000, height = 600)
        st.plotly_chart(fig)

        col1, col2,col3 = st.columns(3)

        sport_select_awa = col2.selectbox(
            "Choose a sport for the following Plot",
            pickle.load(open("w_sports.txt","rb"))
        )

        st.subheader("Winnings on the basis of Height and Weight")
        fig = px.scatter(Athelete_wise_analysis.height_weight_scatter(df,sport_select_awa),x = "Weight",y='Height',color = 'Medal',symbol = 'Sex')
        st.plotly_chart(fig)

        st.subheader("Male vs Female Participation")
        fig = px.line(Athelete_wise_analysis.male_vs_female(df),x = 'Year', y = ['Male','Female'])
        st.plotly_chart(fig)


    elif tab == "Get in Touch with Me":
        contact_form = '''
        <form action="https://formsubmit.co/tokas.2sonu@gmail.com" method="POST">
            <input type="hidden" name="_autoresponse" value="Thank You for spending your valuable time on my website. I will contact you soon.">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_next" value="https://vivek-2567-olympic-games-data-analysis-app-zrn7gl.streamlit.app">
            <input type="text" name="name" id = 'input' placeholder = "Your Name" required>
            <input type="email" name="email" id = 'input' placeholder = "Your Email" required>
            <textarea name = 'message' id = 'input' placeholder = 'Your Message' required></textarea>
            <button onclick="document.getElementById('input').value = ''" type="submit">Send</button>
        </form>
        '''

        st.write("##")
        st.markdown(contact_form,unsafe_allow_html=True)
        local_css("style/style.css")