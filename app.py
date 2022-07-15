import streamlit as st
import preprocess
import re
import stats
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
     page_title="GRAPHOS - insights chats",
     page_icon="✴",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.digitalmonkey.com.br',
         'Report a bug': "https://github.com/tiagomnz/graphos/pulls",
         'About': "# GRAPHOS. Extraindo Insights de conversa!"
     }
 )

#st.image ("https://raw.githubusercontent.com/tiagomnz/graphos/main/graphos.png")
st.sidebar.image("https://raw.githubusercontent.com/tiagomnz/graphos/f20e30a5a30dd9c5d38f3d17261fb62284109383/graphos.svg")
st.sidebar.title("PAINEL")

# Subir arquivo

uploaded_file = st.sidebar.file_uploader("Escolha o arquivo")


if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    #convertendo bytecode em arquivo de texto 

    data = bytes_data.decode("utf-8")

    # encaminhando arquivo para processamento

    df = preprocess.preprocess(data)

    # Exibindo dataframe

    #st.dataframe(df)

    # Capturando usuários
    user_list = df['User'].unique().tolist()

    # removendo notificação do grupo
    # Exibindo usuarios
    # st.dataframe(user_list)
    
    user_list.remove('Group Notification')

    # Organizando 
    user_list.sort()

    # Incluindo dados gerais para análise Todos do grupo

    user_list.insert(0, "Todos")

    selected_user = st.sidebar.selectbox(
        "Mostrar a analise em relação ao", user_list)

    st.title("Analizando conversa de WhatsApp para o usuário " + selected_user)
    if st.sidebar.button("Exibir Analise"):

        # Capturando o estado do usuário selecionado do script

        num_messages, num_words, media_omitted, links = stats.fetchstats(
            selected_user, df)

        # a primeira fase é mostrar as estatísticas básicas como número de usuários, número de mensagens, número de mídia compartilhada e etc. Então para exibir em 4 colunas
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total de Menssagens")
            st.title(num_messages)

        with col2:
            st.header("Total de palavras")
            st.title(num_words)

        with col3:
            st.header("Midia compartilhada")
            st.title(media_omitted)

        with col4:
            st.header("Total de links compartilhados")
            st.title(links)

        # Localizando o usuário mais sobrecarregado

        if selected_user == 'Todos':

            # Divide o espaço em duas colunas

            st.title('Usuário mais ocupado')
            busycount, newdf = stats.fetchbusyuser(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(busycount.index, busycount.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                print ('teste')
                #st.dataframe(newdf)

        # Word Cloud

        st.title('Nuvem de palavras')
        df_img = stats.createwordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_img)
        st.pyplot(fig)


        # Palavras mais comuns - Grafico

        most_common_df = stats.getcommonwords(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Palavras mais comuns')
        st.pyplot(fig)

        # Analise de Emoji

        emoji_df = stats.getemojistats(selected_user, df)
        emoji_df.columns = ['Emoji', 'Count']

        st.title("Analise de Emoji")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            emojicount = list(emoji_df['Count'])
            perlist = [(i/sum(emojicount))*100 for i in emojicount]
            emoji_df['Percentage use'] = np.array(perlist)
            st.dataframe(emoji_df)

        # timeline Mensal

        st.title("Timeline Mensal")
        time = stats.monthtimeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(time['Time'], time['Message'], color='green')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)

        # Mapas de atividade

        st.title("Mapa de atividade")

        col1, col2 = st.columns(2)

        with col1:

            st.header("Dia mais atividades")

            busy_day = stats.weekactivitymap(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

        with col2:

            st.header("Mês com mais atividades")
            busy_month = stats.monthactivitymap(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            #st.bar_chart(busy_month)
            st.pyplot(fig)