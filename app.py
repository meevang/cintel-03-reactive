import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

penguins = load_penguins()

ui.page_opts(title="Mee's Layout", fillable=True)

# Create a single sidebar
with ui.sidebar(open="open", bg="#f8f8f8"):
    # Add a 2nd level header to the sidebar
    ui.h2("Sidebar")

    # Create a dropdown input to choose a column
    ui.input_selectize(
        "selected_attribute",
        label="Select attributes",
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
        selected=["bill_length_mm"],
        multiple=True)
    
    ui.input_numeric("plotly_bin_count", "Input number", 0)
    
    ui.input_slider("seaborn_bin_count", "Bin Count", min=0, max=20, value=10)
    
    ui.input_checkbox_group(
        "selected_species_list",
        "Species:", 
        ["Adelie", "Gentoo", "Chinstrap"],
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
            return render.DataTable(penguins, height='400px')
    
    # Second column: Data Grid
    with ui.card():
        ui.card_header("Penguins Data Grid")
        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(penguins, width='100%', height='400px')


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram: Species")
        
        @render_plotly
        def plotly_histogram():
            return px.histogram(penguins, x="body_mass_g", color="species", 
                                 title="Penguin Body Mass by Species",
                                 labels={"body_mass_g": "Body Mass (g)", "count": "Count"},
                                 marginal="box")

    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram: Species")
    
        @render.plot
        def seaborn_histogram():
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=penguins, x="body_mass_g", hue="species", multiple="stack", ax=ax)
            ax.set_title("Penguin Body Mass by Species")
            ax.set_xlabel("Body Mass (g)")
            ax.set_ylabel("Count")
            return fig

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Penguin Flipper & Bill Length")

    @render_plotly
    def plotly_scatterplot():
        fig = px.scatter(penguins, 
                     x="flipper_length_mm", 
                     y="bill_length_mm", 
                     color="species",
                     labels={"flipper_length_mm": "Flipper Length (mm)",
                             "bill_length_mm": "Bill Length (mm)",
                             "species": "Species"})
        return fig

with ui.card(full_screen=True):
    @render_plotly
    def plot1():
        return px.histogram(px.data.tips(), y="tip")

    @render_plotly
    def plot2():
        return px.histogram(px.data.tips(), y="total_bill")
