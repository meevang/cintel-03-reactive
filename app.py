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


# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    isSpeciesMatch = penguins_df["species"].isin(input.selected_species_list())
    return penguins_df[isSpeciesMatch]


# Additional Python Notes
# ------------------------

# Capitalization matters in Python. Python is case-sensitive: min and Min are different.
# Spelling matters in Python. You must match the spelling of functions and variables exactly.
# Indentation matters in Python. Indentation is used to define code blocks and must be consistent.

# Functions
# ---------
# Functions are used to group code together and make it more readable and reusable.
# We define custom functions that can be called later in the code.
# Functions are blocks of logic that can take inputs, perform work, and return outputs.

# Defining Functions
# ------------------
# Define a function using the def keyword, followed by the function name, parentheses, and a colon. 
# The function name should describe what the function does.
# In the parentheses, specify the inputs needed as arguments the function takes.

# For example:
#    The function filtered_data() takes no arguments.
#    The function between(min, max) takes two arguments, a minimum and maximum value.
#    Arguments can be positional or keyword arguments, labeled with a parameter name.

# The function body is indented (consistently!) after the colon. 
# Use the return keyword to return a value from a function.

# Calling Functions
# -----------------
# Call a function by using its name followed by parentheses and any required arguments.
    
# Decorators
# ----------
# Use the @ symbol to decorate a function with a decorator.
# Decorators a concise way of calling a function on a function.
# We don't typically write decorators, but we often use them.
