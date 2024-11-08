import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shiny import reactive

# Load penguins dataset
penguins = load_penguins()

ui.page_opts(title="Mee's Layout", fillable=True)

# Create a single sidebar
with ui.sidebar(open="open", bg="#f8f8f8"):
    # Add a 2nd level header to the sidebar
    ui.h2("Sidebar")

    # Create a dropdown input to choose a column
    ui.input_select(
    "histogram_attribute",
    label="Select attribute for Ploytly Histogram",
    choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    selected="body_mass_g"
)
    
    ui.input_numeric("plotly_bin_count", "Input number for Plotly Histogram", min=0, max=30, value=0)
    
    ui.input_slider("seaborn_bin_count", "Bin Count for Seaborn Hisogram", min=0, max=20, value=10)
    
    ui.input_checkbox_group(
        "selected_species_list",
        "Species:", 
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True)
    # Use ui.a() to add a hyperlink to the sidebar
    ui.a("GitHub", href="https://github.com/meevang/cintel-02-data", target="_blank")

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr(style="border-top: 10px dashed #38761d;")


with ui.layout_columns():
    # First column: Data Table
    with ui.card():
        ui.card_header("Penguins Data Table")
        @render.data_frame
        def penguins_datatable():
            return render.DataTable(data=filtered_data(), filters=False, height='400px')
    
    # Second column: Data Grid
    with ui.card():
        ui.card_header("Penguins Data Grid")
        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(data=filtered_data(), filters=False, width='100%', height='400px')


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram: Species")
        
        @render_plotly
        def plotly_histogram():
            filtered_df = penguins[penguins['species'].isin(input.selected_species_list())]
            x_attr = input.histogram_attribute()
    
            return px.histogram(filtered_df, 
                        x=x_attr,
                        color="species", 
                        title=f"Penguin {x_attr} by Species",
                        labels={x_attr: x_attr, "count": "Count"},
                        nbins=input.plotly_bin_count(),
                        marginal="box")
            

    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram: Species")
    
        @render.plot
        def seaborn_histogram():
            filtered_df=penguins[penguins['species'].isin(input.selected_species_list())]
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(filtered_df, x="body_mass_g", hue="species", multiple="stack", ax=ax, bins=input.seaborn_bin_count())
            ax.set_title("Penguin Body Mass by Species")
            ax.set_xlabel("Body Mass (g)")
            ax.set_ylabel("Count")
            return fig

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Penguin Flipper & Bill Length")

    @render_plotly
    def plotly_scatterplot():
        filtered_df=penguins[penguins['species'].isin(input.selected_species_list())]
        fig = px.scatter(filtered_df, 
                     x="flipper_length_mm", 
                     y="bill_length_mm", 
                     color="species",
                     labels={"flipper_length_mm": "Flipper Length (mm)",
                             "bill_length_mm": "Bill Length (mm)",
                             "species": "Species"})
        return fig


# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    selected_species = input.selected_species_list()
    return penguins[penguins["species"].isin(selected_species)]
