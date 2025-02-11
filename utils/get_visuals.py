
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def rating_distributions(data):
    rating = data['rating'].value_counts().sort_index()
    rating_norm = data['rating'].value_counts(normalize=True).sort_index()

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Quantitative Rating", "Percentage Rating"))

    fig.add_trace(go.Bar(x=rating, y=rating.index, orientation='h', name='Quantitative Rating'),
                  row=1, col=1)
    fig.add_trace(go.Bar(x=rating_norm, y=rating_norm.index, orientation='h', name='Percentage Rating'),
                  row=1, col=2)

    fig.update_layout(height=500, width=1400,
                      title_text="Rating Distribution")
    fig = pio.to_html(fig, full_html=False)
    return fig

def review_table(data):
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(data.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[data.date, data.review, data.rating, data.title],
                   fill_color='lavender',
                   align='left'))
    ])

    fig = pio.to_html(fig, full_html=False)
    return fig
