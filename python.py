import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def filtros_on_change():
    print('chamou o on_change')
    selected_items = st.session_state['itens_selecionados_filtros']  
    
    mostrar_filtros = st.session_state['mostrar_filtros']  
    
    if selected_items:
        removed_items = set(st.session_state['filtros']) - set(selected_items)
        if removed_items:
            for item in removed_items:
                print(f'passou no remove item do SelectedItems:{item}')                
                st.session_state['filtros'].remove(item)
            st.session_state['mostrar_filtros'] = st.session_state['filtros']
            st.session_state['itens_selecionados_filtros'] = st.session_state['filtros']
    else:
        print('passou no elif selected_itens')
        st.session_state['filtros'] = []
        st.session_state['mostrar_filtros'] = st.session_state['filtros']
        st.session_state['itens_selecionados_filtros'] = st.session_state['filtros']       
    
    if mostrar_filtros:
        removed_items = set(st.session_state['filtros']) - set(mostrar_filtros)
        if removed_items:   
            for item in removed_items:
                print(f'passou no remove item do MostrarFiltros:{item}') 
                st.session_state['filtros'].remove(item)
            st.session_state['mostrar_filtros'] = st.session_state['filtros']
            st.session_state['itens_selecionados_filtros'] = st.session_state['filtros']
    else:
        print('passou no elif mostrar_filtros')
        st.session_state['filtros'] = []
        st.session_state['mostrar_filtros'] = st.session_state['filtros']
        st.session_state['itens_selecionados_filtros'] = st.session_state['filtros']
        
    
  
        
def porcentagem_imoveis_animais(data):
    imoveis_aceitam_animais = data[data['animal']=='acept']    
    porcentagem = (len(imoveis_aceitam_animais) / len(data)) * 100
    return porcentagem

def porcentagem_imoveis_mobiliados(data):
    imoveis_mobiliados = data[data['mobiliado']=='furnished']    
    porcentagem = (len(imoveis_mobiliados) / len(data)) * 100
    return porcentagem
def area_media_imoveis(data):
    area = data['área'].mean()    
    return area

def checar_filtro_na_lista(lista, string):
    return [string in item for item in lista]

@st.dialog("Escolha o filtro")
def escolher_filtro():
    filtro = st.selectbox(
        "Escolha o filtro:",
        ("Área","Quartos", "Banheiros", "Vagas de Estacionamento", "Andar", "Animais", "Mobiliado"),
    )
    
    if filtro == "Andar":
        st.write("Escolha o andar:")
        number = st.number_input("Insert a number",format="%.0f")
        if st.button("Filtrar"):
            st.session_state.filtros.append(f'andar == "{int(number)}"')
            st.rerun()
    
    elif filtro == "Animais":
        animais = st.radio(
            "Local permite animais?",
            ["Sim", "Não"], index=None,
            horizontal=True,
        )
        if animais:
            if animais == "Sim":
                st.session_state.filtros.append(f'animal == "acept"')
                st.rerun()
            if animais == "Não":
                st.session_state.filtros.append(f'animal == "not acept"')
                st.rerun()
                
    elif filtro == "Mobiliado":
        mobiliado = st.radio(
            "O local é mobiliado?",
            ["Sim", "Não"], index=None,
            horizontal=True,
        )
        if mobiliado == "Sim":
            st.session_state.filtros.append(f'mobiliado == "furnished"')
            st.rerun()
        if mobiliado == "Não":
            st.session_state.filtros.append(f'mobiliado == "not furnished"')
            st.rerun()

    elif filtro == "Quartos":
        st.write("Quantidade de quartos")
        operador = st.selectbox(
            " ",
            ("==",">=", "<="),
        )        
        quartos = st.number_input("a:",format="%.0f")
        if st.button("Filtrar") and operador:
            st.session_state.filtros.append(f'quartos {operador} {int(quartos)}')
            st.rerun()

    elif filtro == "Área":
        st.write("Área ")
        operador = st.selectbox(
            " ",
            ("==",">=", "<="),
        )        
        area = st.number_input("a:",format="%.0f")
        if st.button("Filtrar") and operador:
            st.session_state.filtros.append(f'área {operador} {int(area)}')
            st.rerun()
    
    elif filtro == "Banheiros":
        st.write("Quantidade de banheiros ")
        operador = st.selectbox(
            " ",
            ("==",">=", "<="),
        )        
        banheiros = st.number_input("a:",format="%.0f")
        if st.button("Filtrar") and operador:
            st.session_state.filtros.append(f'banheiros {operador} {int(banheiros)}')
            st.rerun()        

    elif filtro == "Vagas de Estacionamento":
        st.write("Vagas de Estacionamento ")
        operador = st.selectbox(
            " ",
            ("==",">=", "<="),
        )        
        vagas = st.number_input("a:",format="%.0f")
        if st.button("Filtrar") and operador:
            st.session_state.filtros.append(f'vagas {operador} {int(vagas)}')
            st.rerun()  
              
def formatar_numeros(value):
    return f'{value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def obter_colunas_selecionadas(options):
    
    colunas = {
        "Condomínio": 'condomínio (R$)',
        "Aluguel": 'aluguel (R$)',
        "IPTU": 'IPTU (R$)',
        "Seguro Incêndio": 'seguro incêndio (R$)',
        "Total": 'total (R$)'
    }
    
    
    colunas_selecionadas = [colunas[opt] for opt in options]
    
    return colunas_selecionadas

if 'filtros' not in st.session_state:
        st.session_state.filtros = []

   
def novo_rerun():
    st.rerun()

data = pd.read_csv('houses_to_rent_v2.csv')

data.rename(columns={
    'city': 'cidade',
    'area': 'área',
    'rooms': 'quartos',
    'bathroom': 'banheiros',
    'parking spaces': 'vagas',
    'floor': 'andar',
    'animal': 'animal',
    'furniture': 'mobiliado',
    'hoa (R$)': 'condomínio (R$)',
    'rent amount (R$)': 'aluguel (R$)',
    'property tax (R$)': 'IPTU (R$)',
    'fire insurance (R$)': 'seguro incêndio (R$)',
    'total (R$)': 'total (R$)'
}, inplace=True)

# Definir o layout para a largura total
st.set_page_config(layout="wide")

#st.write(data['banheiros'].max())

tab1, tab2 = st.tabs(["📈Gráficos", "🗄️ Dados"])

with tab1:
    #expander = st.expander("Clique aqui para ver explicação.")
    #expander.write('''
    #O gráfico abaixo apresenta informações sobre os custos de aluguel na cidade.
    #''')
    if st.session_state['filtros']:
        #print(st.session_state['filtros'])
        expander = st.expander("Base filtrada! Clique aqui para ver os filtros")
        expander.multiselect("Filtrar por:", st.session_state.filtros, st.session_state.filtros,
            placeholder='Clique no botão para adicionar', label_visibility="hidden",
            on_change=filtros_on_change, key='mostrar_filtros'             
            )
        
                #print(st.session_state.filtros)
        filtros_string = " and ".join(st.session_state.filtros)
                #print(filtros_string)
        if filtros_string != "":                
            data = data.query(filtros_string)
            
    st.subheader("Estatísticas Gerais")
    col_metric1, col_metric2,col_metric3, col_metric4 = st.columns(4)
    with col_metric1:
        with st.container(border=True):
            st.metric(label='Quantidade de Imóveis', value=data.shape[0])
    with col_metric2:
        with st.container(border=True):
            st.metric(label='Média de aluguel', value= 'R$ '+formatar_numeros(data['aluguel (R$)'].mean()))
    with col_metric3:
        with st.container(border=True):
            st.metric(label='Imóveis que aceitam animais', value=formatar_numeros(porcentagem_imoveis_animais(data))+"%")
    with col_metric4:
        with st.container(border=True):
            st.metric(label='Imóveis mobiliados', value=formatar_numeros(porcentagem_imoveis_mobiliados(data))+"%")
    
    col_metric5, col_metric6,col_metric7, col_metric8 = st.columns(4)
    
    with col_metric5:
        with st.container(border=True):
            st.metric(label='Área Média dos Imóveis', value=formatar_numeros(area_media_imoveis(data))+' M²')
    with col_metric6:
        with st.container(border=True):
            st.metric(label='Média de Vagas de Estacionamento', value=formatar_numeros(data['vagas'].mean()))
    with col_metric7:
        with st.container(border=True):
            st.metric(label='Média de Condomínio', value='R$ '+formatar_numeros(data['condomínio (R$)'].mean()))
    with col_metric8:
        with st.container(border=True):
            st.metric(label='Média do Valor Total', value='R$ '+formatar_numeros(data['total (R$)'].mean()))
    
    
    with st.container():        
        #st.write("You selected:", options)  
             
              
        st.subheader('Custos totais de aluguel por cidade')
        
        coluna3, coluna4 = st.columns(2)
        
        with coluna3:
                       
            options = st.multiselect(
                "Adicionar custos de:",
                ["Condomínio", "Aluguel", "IPTU", "Seguro Incêndio", "Total"],
                ["Aluguel"],
            )
        
        with coluna4:
            adicionar = st.radio(
            "Exibir:",
            ["Média", "Mínimo", "Máximo"],
            index=0, horizontal=True,
        )
        #st.write(type(options))
               
        if adicionar == "Média":
        # Gráfico de barras para a média de aluguel por cidade
            if 'filtros' in st.session_state:
                #print(st.session_state.filtros)
                filtros_string = " and ".join(st.session_state.filtros)
                #print(filtros_string)
                if filtros_string != "":                
                    data = data.query(filtros_string)                
            #st.write(data)
            mean_values_by_city = data.groupby('cidade')[obter_colunas_selecionadas(options)].mean().reset_index()

            
            
            fig, ax = plt.subplots(figsize=(12, 6))
            mean_values_by_city.plot(kind='bar', ax=ax)
            ax.set_title('Valores Médios de Aluguel por Cidade')
            ax.set_xlabel('Cidade')
            ax.set_ylabel('Valor Médio (R$)')
            ax.set_xticklabels(mean_values_by_city.cidade, rotation=0)
            ax.legend(title='Métricas')
            for container in ax.containers:
                labels = ax.bar_label(container, labels=[formatar_numeros(val) for val in container.datavalues], label_type='edge')
                for label in labels:
                    label.set_rotation(90)
            st.pyplot(fig)
            
        if adicionar == "Mínimo":
            if 'filtros' in st.session_state:
                #print(st.session_state.filtros)
                filtros_string = " and ".join(st.session_state.filtros)
                #print(filtros_string)
                if filtros_string != "":                
                    data = data.query(filtros_string) 
        
            mean_values_by_city = data.groupby('cidade')[obter_colunas_selecionadas(options)].min().reset_index()

            
           
            fig, ax = plt.subplots(figsize=(12, 6))
            mean_values_by_city.plot(kind='bar', ax=ax)
            ax.set_title('Valores mínimos de Aluguel por Cidade')
            ax.set_xlabel('Cidade')
            ax.set_ylabel('Valor Mínimo (R$)')
            ax.set_xticklabels(mean_values_by_city.cidade, rotation=45)
            ax.legend(title='Métricas')
            for container in ax.containers:
                labels = ax.bar_label(container, labels=[formatar_numeros(val) for val in container.datavalues], label_type='edge')
                for label in labels:
                    label.set_rotation(90)
            
            fig.tight_layout()
            st.pyplot(fig)
            
        if adicionar == "Máximo":
            if 'filtros' in st.session_state:
                #print(st.session_state.filtros)
                filtros_string = " and ".join(st.session_state.filtros)
                #print(filtros_string)
                if filtros_string != "":                
                    data = data.query(filtros_string) 
        
            mean_values_by_city = data.groupby('cidade')[obter_colunas_selecionadas(options)].max().reset_index()

            
            
            fig, ax = plt.subplots(figsize=(12, 6))
            mean_values_by_city.plot(kind='bar', ax=ax)
            ax.set_title('Valores Máximos de Aluguel por Cidade')
            ax.set_xlabel('Cidade')
            ax.set_ylabel('Valor Máximo (R$)')
            ax.set_xticklabels(mean_values_by_city.cidade, rotation=45)
            ax.legend(title='Métricas')
            
            #values = mean_values_by_city['total (R$)']
            #max_value = values.max()
            #threshold = 0.8 * max_value
        # for container in ax.containers:
            #    labels = ax.bar_label(container, labels=[formatar_numeros(val) for val in container.datavalues], label_type='edge')
            #    for label, bar in zip(labels, container):
            #        height = bar.get_height()
            #        if height <= threshold:
            #           label.set_rotation(90)
            for container in ax.containers:
                labels = ax.bar_label(container, labels=[formatar_numeros(val) for val in container.datavalues], label_type='edge')
                for label in labels:
                    label.set_rotation(90)
            fig.tight_layout()
            st.pyplot(fig)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        data.boxplot(column='aluguel (R$)', by='cidade', grid=False, ax=ax1)
        ax1.set_title('Distribuição dos Valores de Aluguel por Cidade')
        plt.suptitle('')  
        ax1.set_xlabel('Cidade')
        ax1.set_ylabel('Aluguel (R$)')
        #plt.xticks(rotation=45)

       
        st.pyplot(fig1)
                    
    with col2:
        df = data[data['andar'] != '-']
        df['andar'] = pd.to_numeric(df['andar'])
        avg_total_by_floor = df.groupby('andar')['total (R$)'].mean().reset_index()

        fig2, ax2 = plt.subplots(figsize=(12, 6))
        ax2.plot(avg_total_by_floor['andar'], avg_total_by_floor['total (R$)'], marker='o')
        ax2.set_title('Evolução dos Custos Totais por Andar')
        ax2.set_xlabel('Andar')
        ax2.set_ylabel('Custo Total (R$)')
        ax2.grid(True)

        st.pyplot(fig2)



with tab2:
    with st.container():
        coluna1, coluna2 = st.columns(2)
        with coluna1:
            filtros = st.multiselect(
                "Filtrar por:", st.session_state.filtros, st.session_state.filtros,
            placeholder='Clique no botão para adicionar', label_visibility="hidden",
            on_change=filtros_on_change, key='itens_selecionados_filtros'             
            )
            
        with coluna2:
            st.write('')
            st.write('')
            if st.button("Adicionar Filtro"):
                escolher_filtro()
        st.write(data)
  