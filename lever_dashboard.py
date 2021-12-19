import pandas as pd
import dash
import dash_html_components as html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import plotly.figure_factory as ff

app = dash.Dash(__name__, external_stylesheets=[
        dbc.themes.LITERA
    ], url_base_pathname='/i_am_the_mayor/'
)
server = app.server

df = pd.read_csv('nyc-jobs.csv')

#top job categories
df['Salary'] = df[['Salary Range From', 'Salary Range To']].mean(axis=1)
counts = df.groupby('Job Category')['Salary'].mean()
counts_list = df['Job Category'].value_counts()
#print(counts.head())
counts_df = pd.DataFrame(counts_list)
counts_salary_df = pd.DataFrame(counts)
df2 = pd.merge(counts_df, counts_salary_df, left_index=True, right_index=True)
df2.sort_values(by=['Job Category'],ascending = True, inplace = True)
fig = px.bar(df2, y=df2.index[-10:], x=df2['Job Category'].tail(10),
            color = df2['Salary'].tail(10), 
            title='Industries by number of postings:', 
            labels={
                     "x": "Number of postings",
                      "y": ' ',
                     "color": "Mean Salary ($)"
                 },
             color_continuous_scale= px.colors.sequential.Sunset)


#Salary range distribution
salary_counts = df['Salary Range To'].value_counts()
salary_counts = pd.DataFrame(counts)
group_labels = ['Salary Range From','Salary Range To']
fig3 = ff.create_distplot([
    df['Salary Range From'],
    df['Salary Range To']], 
    group_labels, bin_size= 10000)

fig4 = go.Figure()
fig4.add_trace(go.Box(y=df['Salary Range From'], name='Salary Range From',
                marker_color = 'indianred'))
fig4.add_trace(go.Box(y=df['Salary Range To'], name = 'Salary Range To',
                marker_color = 'lightseagreen'))

# # of positions
df.sort_values(by = ['# Of Positions'], ascending = True, inplace = True)
df_group = df.groupby(['Business Title']).mean(['# Of Positions'])
df_group.sort_values('# Of Positions', ascending = True, inplace = True)
df_group.index = df_group.index.str.capitalize()

df['Salary_calc'] = ((df['Salary Range From'] + df['Salary Range To']) / 2)
average_salary_calc = (df['Salary_calc'].sum() / len(df))
average_salary_calc = average_salary_calc.round(2)
        
app.layout = html.Div(
    [
    html.H1("New York City Job Postings", 
    style = {'text-align': 'center',"text-decoration" :"underline"}
    ),
    html.Div(id = 'total_jobs'),
    html.Br(),
    html.P('Incumbent Mayor: Cam Deardon (Independent)',     
    style = {'text-align': 'center','font-family':'helvetica'}),
    html.Div([html.H4('Total Jobs: ', style={'text-align': 'center',
    'font-weight': 'light'}),
    html.P(str(len(df)), style=
    {'text-align': 'center','font-family': 'helvetica'}),
    html.H4('Average Salary: ', style={'text-align': 'center',
    'font-weight': 'light'}),
    html.P('$' + str(average_salary_calc), style=
    {'text-align': 'center','font-family': 'helvetica'})], 
    className="h-100 p-5 text-white bg-dark rounded-3"),
    html.Br(),
        html.Div(
            dbc.Row(children=[
                dbc.Col(
                children=[
                    html.Div(
                        children=[
                            dcc.Tabs(id="tabs-graph", value='tab-1-graph', children=[
                            dcc.Tab(label='Top Sectors', value='tab-1-graph'),
                            dcc.Tab(label='Top Agencies', value='tab-2-graph'),
                            dcc.Tab(label='Top Divisions', value='tab-3-graph')
                            ]),dcc.Graph(id='tabs-content-graph', figure = {})
                                ]
                            )
                        ], width=8),
        dbc.Col(
            children=[
                    html.Div(
                        children=[
                                html.Div(
                                    [html.P('Job posting type report', 
                                    style={'text-align':'center', 'font-family': 'helvetica'}
                                            )
                                    ]
                                    ),
                                dcc.Dropdown(id='report_type', 
                                    options=[
                                            {'label': 'Full vs part time ', 'value': 'OPT1'},
                                            {'label': 'Internal vs external', 'value': 'OPT2'}
                                            ],
                                    placeholder='Select a report type',
                                    value='OPT1',
                                    multi=False,
                                    clearable=False,
                                    style={ 
                                    'text-align-last':'center'}),

                                    dcc.Graph(id='report_type_', figure = {})
                        ]
                    )
            ],width={'size':4, 'offset':.5})
            ]
            )
        ),

html.Br(),
html.Br(),
html.Div(
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    html.Div(
                        children=[
                        #Salary Distributions
                        html.H4('Salary Distribution across all jobs', style={
                        'font-family': 'helvetica', 'text-align-last':'center'}),
                                    dcc.Dropdown(id='salary_visuals', 
                                        options=[
                                        {'label': 'Distribution Plot', 'value': 'OPT1'},
                                        {'label': 'Box Plot', 'value': 'OPT2'}
                                        ],
                                        value='OPT1',
                                        placeholder='Select a report type',
                                        multi=False,
                                        clearable=False,
                                        style={ 
                                        'text-align-last':'center'
                                        }
                                        ),

                                        dcc.Graph(id='salary_distribution', 
                                        figure = {})
                            ]
                        )
                    ], width=7),
                    dbc.Col(
                children=[
                    html.Div(
                        children=[
                            html.H4('Top 5 highest vacancy jobs: ', 
                            style={ 
                            'text-align': 'center',
                            'font-family':'helvetica'}
                                ),
                            dcc.RadioItems(
                                id='hourly_vs_annual',
                                options=[
                                {'label': 'Hourly Salary', 'value': 'OPT1'},
                                {'label': 'Annual Salary', 'value':'OPT2'}
                            ], value='OPT2',
                            labelStyle={'display': 'flex'}
                        ),
                        dcc.Graph(id='hourly_vs_annual_', figure={}
                                    )
                                ]
                            )
                ],width=5),
            ]
        )
    ),
html.Div(className="h-100 p-5 text-white bg-dark rounded-3")

]
)

@app.callback(Output('tabs-content-graph', 'figure'),
              Input('tabs-graph', 'value'))

def render_content(tab):
    df['Salary'] = df[['Salary Range From', 'Salary Range To']].mean(axis=1)
    counts = df.groupby('Agency')['Salary'].mean()
    counts_list = df['Agency'].value_counts()
    #print(counts.head())
    counts_df = pd.DataFrame(counts_list)
    counts_salary_df = pd.DataFrame(counts)
    df2 = pd.merge(counts_df, counts_salary_df, left_index=True, right_index=True)
    df2.sort_values(by=['Agency'],ascending = True, inplace = True)
    df2.index = df2.index.str.capitalize()

    fig_agency = px.bar(df2, y=df2.index[-10:], x=df2['Agency'].tail(10),
                        
                color = df2['Salary'].tail(10), 
                title='Industries by number of postings:', 
                labels={
                        "x": "Number of postings",
                        "y": " ",
                        "color": "Mean Salary ($)"
                    },
                color_continuous_scale= px.colors.sequential.Sunset)

    df['Salary_'] = df[['Salary Range From', 'Salary Range To']].mean(axis=1)
    counts2 = df.groupby('Division/Work Unit')['Salary'].mean()
    counts_list2 = df['Division/Work Unit'].value_counts()
    #print(counts.head())
    counts_df2 = pd.DataFrame(counts_list2)
    counts_salary_df2 = pd.DataFrame(counts2)
    df3 = pd.merge(counts_df2, counts_salary_df2, left_index=True, right_index=True)
    df3.sort_values(by=['Division/Work Unit'],ascending = True, inplace = True)
    df3.index = df3.index.str.capitalize()

    fig_division = px.bar(df3, y=df3.index[-10:], x=df3['Division/Work Unit'].tail(10),
                        
                color = df2['Salary'].tail(10), 
                title='Industries by number of postings:', 
                labels={
                        "x": "Number of postings",
                        "y": " ",
                        "color": "Mean Salary ($)"
                    },
                color_continuous_scale= px.colors.sequential.Sunset)

    if tab == 'tab-1-graph':
        return fig
    elif tab == 'tab-2-graph':
        return fig_agency
    else:
        return fig_division


@app.callback(
    Output(component_id='report_type_', component_property='figure'),
    [Input(component_id='report_type', component_property='value')]
)

def update_graph(report_type):
    dff = df
    if report_type == 'OPT1':
        ft_pt = dff['Full-Time/Part-Time indicator']
        ft_pt.fillna('Not listed', inplace = True)
        ft_pt.replace('F', 'Full Time', inplace = True)
        ft_pt.replace('P', 'Part Time', inplace = True)
        value_counts_ft_pt = dff['Full-Time/Part-Time indicator'].value_counts()
        labels_ft_pt = value_counts_ft_pt.index.tolist()
        #full time vs part time
        fig1 = px.pie(dff, 
        values = value_counts_ft_pt, 
        names = labels_ft_pt,hole=.5)

        return fig1

    else:
         #internal vs externl
        value_counts_posting_type = dff['Posting Type'].value_counts()
        labels_posting_type = value_counts_posting_type.index.tolist()
        fig2 = px.pie(
        df, 
            values = value_counts_posting_type, 
            names = labels_posting_type, 
            color_discrete_sequence=px.colors.sequential.Sunset,hole=.5)
        
        return fig2
@app.callback(
    Output(component_id='salary_distribution', component_property='figure'),
    [Input(component_id='salary_visuals', component_property='value')]
)
def update_salary_visuals(salary_visuals):
    if salary_visuals == 'OPT1':
        return fig3
    else:
        return fig4 

@app.callback(
    Output('hourly_vs_annual_', 'figure'),
    [Input('hourly_vs_annual', 'value')]
)
def update_salary_visuals(hourly_vs_annual):
    dff = df
    df_salary1 = dff[dff['Salary Frequency'] == 'Hourly']
    df_salary1.sort_values(by = ['# Of Positions'], ascending = True, inplace = True)
    df_group1 = df_salary1.groupby(['Business Title']).mean(['# Of Positions'])
    df_group1.sort_values('# Of Positions', ascending = True, inplace = True)
    df_group1.index = df_group1.index.str.capitalize()
    df_salary1.sort_values(by = ['# Of Positions'], ascending = True, inplace = True)
    df_group1 = df_salary1.groupby(['Business Title']).mean(['# Of Positions'])
    df_group1.sort_values('# Of Positions', ascending = True, inplace = True)
    df_group1.index = df_group1.index.str.capitalize()
    df_group1['Salary'] = df_group1[['Salary Range From', 'Salary Range To']].mean(axis=1)
    df_group1.sort_values(by='# Of Positions', ascending = True, inplace = True)
    fig5 = px.bar(df, x=df_group1.index[-5:], y=df_group1['# Of Positions'][-5:],
    color=df_group1['Salary'][-5:], 
    color_continuous_scale= px.colors.sequential.Sunset, 
                    labels={
                        "y": "Number of Vacancies",
                        "x": " ",
                        "color": "Mean Salary ($)"
                    })
    df_salary2 = dff[dff['Salary Frequency'] == 'Annual']
    df_salary2.sort_values(by = ['# Of Positions'], ascending = True, inplace = True)
    df_group2 = df_salary2.groupby(['Business Title']).mean(['# Of Positions'])
    df_group2.sort_values('# Of Positions', ascending = True, inplace = True)
    df_group2.index = df_group2.index.str.capitalize()
    df_salary2.sort_values(by = ['# Of Positions'], ascending = True, inplace = True)
    df_group2 = df_salary2.groupby(['Business Title']).mean(['# Of Positions'])
    df_group2.sort_values('# Of Positions', ascending = True, inplace = True)
    df_group2.index = df_group2.index.str.capitalize()
    df_group2['Salary'] = df_group2[['Salary Range From', 'Salary Range To']].mean(axis=1)
    df_group2.sort_values(by='# Of Positions', ascending = True, inplace = True)
    fig6 = px.bar(dff, x=df_group2.index[-5:], y=df_group2['# Of Positions'][-5:],
    color=df_group2['Salary'][-5:],
    color_continuous_scale= px.colors.sequential.Sunset, 
    labels={
                        "y": "Number of Vacancies",
                        "x": " ",
                        "color": "Mean Salary ($)"})

    if hourly_vs_annual == 'OPT1':
        return fig5
    else:
        return fig6


if __name__ == '__main__':
    app.run_server(debug=True)
