import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv('dataset_asimov.csv')

df.loc[ df['Mês'] == 'Jan', 'Mês'] = 1
df.loc[ df['Mês'] == 'Fev', 'Mês'] = 2
df.loc[ df['Mês'] == 'Mar', 'Mês'] = 3
df.loc[ df['Mês'] == 'Abr', 'Mês'] = 4
df.loc[ df['Mês'] == 'Mai', 'Mês'] = 5
df.loc[ df['Mês'] == 'Jun', 'Mês'] = 6
df.loc[ df['Mês'] == 'Jul', 'Mês'] = 7
df.loc[ df['Mês'] == 'Ago', 'Mês'] = 8
df.loc[ df['Mês'] == 'Set', 'Mês'] = 9
df.loc[ df['Mês'] == 'Out', 'Mês'] = 10
df.loc[ df['Mês'] == 'Nov', 'Mês'] = 11
df.loc[ df['Mês'] == 'Dez', 'Mês'] = 12

df['Chamadas Realizadas'] = df['Chamadas Realizadas'].astype(int)
df['Dia'] = df['Dia'].astype(int)
df['Mês'] = df['Mês'].astype(int)

df['Valor Pago'] = df['Valor Pago'].str.lstrip('R$')
df['Valor Pago'] = df['Valor Pago'].astype(int)

df.loc[df['Status de Pagamento'] == 'Pago','Status de Pagamento'] = 1
df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0

df['Status de Pagamento'] = df ['Status de Pagamento'].astype(int)

# Valor do mes
df1 = df.groupby('Equipe')['Valor Pago'].sum().reset_index()

fig1 = go.Figure(go.Bar(
    x=df1['Valor Pago'],
    y=df1['Equipe'],
    orientation='h',
    textposition='auto',
    text=df1['Valor Pago'],
    insidetextfont=dict(family='Times', size=12)))

#Chamadas médias por dia do mes

df2 = df.groupby('Dia')['Chamadas Realizadas'].sum().reset_index()

fig2 = go.Figure(go.Scatter(
    x=df2['Dia'],y=df2['Chamadas Realizadas'], mode='lines',fill='tonexty'))

fig2.add_annotation(text='Chamadas Médias por dia do Mês',
    xref="paper", yref="paper",
    font=dict(
        size=20,
        color='gray'),                
    align="center", bgcolor="rgba(0,0,0,0.8)",
    x=0.05, y=0.85, showarrow=False)
fig2.add_annotation(text=f"Média : {round(df2['Chamadas Realizadas'].mean(),2)}",
    xref="paper", yref="paper",
    font=dict(
       size=30,
       color='gray'
    ),
    align="center", bgcolor="rgba(0,0,0,0.8)",
    x=0.05, y=0.55, showarrow=False)

#Chamadas médias por mês

df3 = df.groupby('Mês')['Chamadas Realizadas'].sum().reset_index()
fig3 = go.Figure(go.Scatter(x=df3['Mês'], y=df3['Chamadas Realizadas'], mode='lines', fill='tonexty'))

fig3.add_annotation(text='Chamadas Médias por Mês',
        xref="paper", yref="paper",
        font=dict(
            size=20,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.85, showarrow=False)
fig3.add_annotation(text=f"Média : {round(df3['Chamadas Realizadas'].mean(), 2)}",
        xref="paper", yref="paper",
        font=dict(
            size=30,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False
)

#Valores pagos por meio de propaganda
df4 = df.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
fig4 = px.line(df4,y="Valor Pago", x="Mês", color="Meio de Propaganda")
fig4.show()

# Propaganda em PieChart // talvez botar no msm card

df5 = df.groupby('Meio de Propaganda')['Valor Pago'].sum().reset_index()
fig5 = go.Figure()
fig5.add_trace(go.Pie(labels=df5['Meio de Propaganda'], values=df5['Valor Pago'], hole=.7))

# Ganhos por Mês + segregação por equipe

df.columns
df6 = df.groupby(['Mês','Equipe'])['Valor Pago'].sum().reset_index()
df6_group = df.groupby('Mês')['Valor Pago'].sum().reset_index()

fig6 = px.line(df6, y="Valor Pago", x="Mês", color="Equipe")
fig6.add_trace(go.Scatter(y=df6_group['Valor Pago'], x=df6_group['Mês'], mode='lines+markers', fill='tonexty', fillcolor='rgba(255,0,0,0.2)',name='Total de Vendas'))
fig6.show()

# Pagos e não pagos

df7 =df.groupby('Status de Pagamento')['Chamadas Realizadas'].sum()
fig7 = go.Figure()
fig7.add_trace(go.Pie(labels=['Não Pago', 'Pago'], values=df7, hole=.6))
fig7.show()

# INDICATORS

df8 = df.groupby(['Consultor', 'Equipe'])['Valor Pago'].sum()
df8.sort_values(ascending=False, inplace=True)
df8 = df8.reset_index()


