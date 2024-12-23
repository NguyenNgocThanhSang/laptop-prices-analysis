import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple
import altair as alt
from math import floor

class Dashboard:
    """
    Dashboard class for laptop price predictions
    """
    def __init__(self) -> None:
        """Initialize dashboard configuration"""
        st.set_page_config(
            page_title="Laptop Price Prediction",
            page_icon="💻",
            layout="wide"
        )

        # Center streamlit column as default
        st.markdown("""
            <style>
                .stColumn {
                    text-align: center
                }
                [data-testid="stMetricLabel"] {
                    display: block
                }
                [data-testid="stFullScreenFrame"], [data-testid="stCaptionContainer"] {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
            </style>
        """, unsafe_allow_html=True)

        self.data: pd.DataFrame = self._load_data()
        
    def _load_data(self) -> pd.DataFrame:
        """
        Load the laptop price data
        
        Returns:
            pd.DataFrame: Loaded price data
        """
        try:
            return pd.read_csv("../Data/processed_data.csv")
        except FileNotFoundError:
            st.error("Data file not found. Please check the file path.")
            return pd.DataFrame()

    def create_overview_section(self) -> None:
        """
        Create the data overview section
        """
        total_laptops = len(self.data)
        total_laptop_brands = self.data['Brand'].nunique()
        total_processor_brands = self.data['Processor_Brand'].nunique()
        total_gpu_brands = self.data['GPU_Brand'].nunique()
        HDD_average = floor(self.data['HDD'].mean())
        SSD_average = floor(self.data['SSD'].mean())
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.metric(label="Number of Laptop", value=total_laptops)
        with col2:
            st.metric(label="Number of  Brand", value=total_laptop_brands)
        with col3:
            st.metric(label="Number of Processor Brand", value=total_processor_brands)
        with col4:
            st.metric(label="Number of GPU Brand", value=total_gpu_brands)
        with col5:
            st.metric(label="Average of HDD Storage", value=HDD_average)
        with col6:
            st.metric(label="Average of SSD Storage", value=SSD_average)

    def create_price_brand_plot(self) -> None:
        """
        Create average price by brand bar plot 
        """
        grouped_df = self.data.groupby('Brand')['Price_VND'].mean().reset_index()
        sorted_df = grouped_df.sort_values('Price_VND', ascending=False).head(10)
        
        chart = alt.Chart(sorted_df).mark_bar().encode(y=alt.Y("Brand", sort=None, title="Brand"), 
                                                   x=alt.X("Price_VND", title="Price (VND)", axis=alt.Axis(format=",.3~s")))
        
        text = alt.Chart(sorted_df).mark_text(
            align='left',  
            dx=5,  
            fontSize=12  
        ).encode(
            y=alt.Y("Brand", sort=None),
            x="Price_VND:Q",  
            text=alt.Text("Price_VND:Q", format=",.3~s")  
        )

        final_chart = chart + text
        
        st.caption("Average Price of Laptop by Brand")
        st.altair_chart(final_chart , use_container_width=False)

    def create_price_processor_plot(self) -> None:
        """
        Create average price by process brand bar plot 
        """
        grouped_df = self.data.groupby('Processor_Brand')['Price_VND'].mean().reset_index()
        sorted_df = grouped_df.sort_values('Price_VND', ascending=False).head(10)
        
        chart = alt.Chart(sorted_df).mark_bar().encode(y=alt.Y("Processor_Brand", sort=None, title="Processor Brand"), 
                                                   x=alt.X("Price_VND", title="Price (VND)", axis=alt.Axis(format=",.3~s")))
        
        text = alt.Chart(sorted_df).mark_text(
            align='left',  
            dx=5,  
            fontSize=12  
        ).encode(
            y=alt.Y("Processor_Brand", sort=None),
            x="Price_VND:Q",  
            text=alt.Text("Price_VND:Q", format=",.3~s")  
        )

        final_chart = chart + text
        
        st.caption("Average Price of Laptop by Processor Brand")
        st.altair_chart(final_chart , use_container_width=False)

    def create_price_gpu_plot(self) -> None:
        """
        Create average price by processbrand bar plot 
        """
        grouped_df = self.data.groupby('GPU_Brand')['Price_VND'].mean().reset_index()
        sorted_df = grouped_df.sort_values('Price_VND', ascending=False).head(10)
        
        chart = alt.Chart(sorted_df).mark_bar().encode(y=alt.Y("GPU_Brand", sort=None, title="GPU Brand"), 
                                                   x=alt.X("Price_VND", title="Price (VND)", axis=alt.Axis(format=",.3~s")))
        
        text = alt.Chart(sorted_df).mark_text(
            align='left',  
            dx=5,  
            fontSize=12  
        ).encode(
            y=alt.Y("GPU_Brand", sort=None),
            x="Price_VND:Q",  
            text=alt.Text("Price_VND:Q", format=",.3~s")  
        )

        final_chart = chart + text

        st.caption("Average Price of Laptop by GPU Brand")
        st.altair_chart(final_chart , use_container_width=False)

    def create_price_group_section(self) -> None:
        col1, col2, col3 = st.columns(3)

        with col1:
            self.create_price_brand_plot()
        with col2:
            self.create_price_processor_plot()
        with col3:
            self.create_price_gpu_plot()

    def create_display_type_bar(self) -> None:
        fig = px.bar(self.data.groupby('Display_type').agg({'Price_VND': 'mean'}).reset_index(), 
             x='Display_type', y='Price_VND')
        fig.update_layout(xaxis_title="Display Type", yaxis_title="Price (VND)", height=300)
        st.caption("Average Price by Display Type")
        st.plotly_chart(fig)

    def create_os_price_plot(self) -> None:
        grouped_df = self.data.groupby('OS')['Price_VND'].mean().reset_index()
        sorted_df = grouped_df.sort_values('Price_VND', ascending=False).head(10)
        
        chart = alt.Chart(sorted_df).mark_bar().encode(y=alt.Y("OS", sort=None, title="GPU Brand"), 
                                                   x=alt.X("Price_VND", title="Price (VND)", axis=alt.Axis(format=",.3~s")))
        
        text = alt.Chart(sorted_df).mark_text(
            align='left',  
            dx=5,  
            fontSize=12  
        ).encode(
            y=alt.Y("OS", sort=None),
            x="Price_VND:Q",  
            text=alt.Text("Price_VND:Q", format=",.3~s")  
        )

        final_chart = chart + text

        st.caption("Average Price of Laptop by Operating system")
        st.altair_chart(final_chart , use_container_width=False)

    def create_brand_pie_chart(self) -> None:
        grouped_df = self.data.groupby('Brand')['Price_VND'].mean().reset_index()
        sorted_df = grouped_df.sort_values('Price_VND', ascending=False).head(5)

        fig = px.pie(sorted_df, values='Price_VND', names='Brand')
        fig.update_layout(
            width=400,  
            height=300
        )

        st.caption("Brand distribution by Price")
        st.plotly_chart(fig)

    def create_pie_section(self) -> None:
        col1, col2, col3 = st.columns(3)

        with col1:
            self.create_display_type_bar()
        with col2:
            self.create_os_price_plot()
        with col3:
            self.create_brand_pie_chart()

    def render(self) -> None:
        """Render the complete dashboard"""
        st.title("Laptop Price Analysis Dashboard")

        self.create_overview_section()
        self.create_price_group_section()
        self.create_pie_section()

def main() -> None:
    """Main function to run the dashboard"""
    dashboard = Dashboard()
    dashboard.render()

if __name__ == "__main__":
    main()