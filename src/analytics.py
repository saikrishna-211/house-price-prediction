import plotly.express as px
import plotly.graph_objects as go


# ------------------------------------------------
# PRICE DISTRIBUTION
# ------------------------------------------------
def price_distribution(df):

    fig = px.histogram(
        df,
        x="price",
        nbins=50,
        title="Property Price Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    return fig


# ------------------------------------------------
# BHK ANALYSIS
# ------------------------------------------------
def bhk_analysis(df):

    fig = px.box(
        df,
        x="bhk",
        y="price",
        title="BHK vs Price Analysis"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    return fig


# ------------------------------------------------
# CORRELATION HEATMAP
# ------------------------------------------------
def correlation_heatmap(df):

    corr_df = df[
        ['total_sqft', 'bath', 'bhk', 'price']
    ]

    correlation = corr_df.corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=correlation.values,
            x=correlation.columns,
            y=correlation.columns,
            text=correlation.values.round(2),
            texttemplate="%{text}"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        title="Feature Correlation Heatmap",
        height=500
    )

    return fig