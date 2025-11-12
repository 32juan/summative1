import pandas as pd
import matplotlib.pyplot as plt
from shiny import App, render, ui

df = pd.read_csv("attendance_anonymised-1.csv")

df = df.rename(columns={
    'Person Code': 'Person Code',
    'Unit Instance Code': 'Module Code',
    'Calocc Code': 'Year',
    'Surname': 'Surname',
    'Forename': 'Forename',
    'Long Description': 'Module Name',
    'Register Event ID': 'Event ID',
    'Object ID': 'Object ID',
    'Register Event Slot ID': 'Event Slot ID',
    'Planned Start Date': 'Date',
    'is Positive': 'Has Attended',
    'Postive Marks': 'Attended',
    'Negative Marks': 'NotAttended',
    'Usage Code': 'Attendance Code'
})
df['Date'] = pd.to_datetime(df['Date'])

module_name = "Spanish"
spanish_df = df[df['Module Name'] == module_name]
ad = spanish_df.groupby('Date')['Attended'].mean()
#same as info from notebook for coloumns and attendance rate calc

app_ui = ui.page_fluid(
    ui.h2("Attendance Rate Chart for Spanish"),
    ui.input_date_range(
        "dates", "Pick Date Range:",
        start=ad.index.min().date(),
        end=ad.index.max().date()
    ),
    ui.input_radio_buttons(
        "chart_type", "Chart type",
        choices=["Line", "Bar"],
        selected="Line"
    ),
    ui.output_plot("attendance_plot")
)
#interactive functions and space for chart

def server(input, output, session):
    @output()
    @render.plot
    def attendance_plot():
        start, end = input.dates()
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)
        mask = (ad.index >= start) & (ad.index <= end)
        plot_data = ad.loc[mask]

        fig, ax = plt.subplots(figsize=(10,5))

        if input.chart_type() == "Line":
            plot_data.plot(ax=ax, marker='o')
        else:
            plot_data.index = plot_data.index.strftime('%Y-%m-%d')
            plot_data.plot.bar(ax=ax)
            #format date labels for bar chart

        ax.set_title("Attendance Rate Over Time for Spanish")
        ax.set_xlabel("Date")
        ax.set_ylabel("Average Attendance Rate")
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        return fig
    #chart formatting

app = App(app_ui, server)