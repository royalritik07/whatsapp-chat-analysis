import streamlit as st
import matplotlib.pyplot as plt
import preprocessing, helper
import seaborn as sns


from helper import most_common_words

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessing.preprocess(data)


    # fetching unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # start area
        st.title('Top Statics')
        num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(links)

        #Monthly Timeline
        timeline = helper.monthly_timeline(selected_user, df)
        st.title('Monthly Timeline')
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)


        #Daily Timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        #activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation=90)
            ax.bar(busy_day.index, busy_day.values, color='yellow')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        st.title('Weekly Activity HeatMap')
        sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #finding the busiest person in the group
        if selected_user == 'Overall':
            st.title('Most busy user')
            x,new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        # wordcloud
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

#   Most common words
    most_common_df = most_common_words(selected_user, df)

    fig, ax = plt.subplots()
    st.title('Most Common Words')
    ax.barh(most_common_df[0], most_common_df[1], color='red')
    plt.xticks(rotation=90)
    st.pyplot(fig)

#     emoji analysis
    emoji_df = helper.emoji_helper(selected_user, df)
    st.title('Emoji Analysis')

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(), autopct='%1.1f%%')
        st.pyplot(fig)