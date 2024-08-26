import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os

# Title of the app
st.title("3D Image Visualizer")

# Sidebar for folder selection
st.sidebar.header("Folder Selection")

# Checkbox for using default folder
use_default_folder = st.sidebar.checkbox("Use default folder")

# Define the default folder path
default_folder_path = '3DSpiral.py'

# Input for folder path
if use_default_folder:
    folder_path = default_folder_path
else:
    folder_path = st.sidebar.text_input("Enter the path of the folder containing .npy file:")

if folder_path:
    # Ensure the directory exists
    if os.path.isdir(folder_path):
        # List .npy files in the folder
        files = [f for f in os.listdir(folder_path) if f.endswith('.npy')]
        
        if files:
            # Dropdown to select a .npy file
            selected_file = st.sidebar.selectbox("Select a .npy file", files)
            
            # Load the selected file
            file_path = os.path.join(folder_path, selected_file)
            data = np.load(file_path, allow_pickle=True)
            
            # Sidebar for slice settings
            st.sidebar.header("Slice Settings")

            # Select the axis for slicing
            axis = st.sidebar.selectbox("Select axis for slicing", options=[0, 1, 2])

            # Select the index for slicing along the chosen axis
            slice_index = st.sidebar.slider(f"Select slice index along axis {axis}", 0, data.shape[axis] - 1, 0)

            # Get the 2D slice
            if axis == 0:
                slice_2d = data[slice_index, :, :]
            elif axis == 1:
                slice_2d = data[:, slice_index, :]
            else:
                slice_2d = data[:, :, slice_index]

            # Display the 2D slice using Plotly
            st.subheader(f"2D Slice along axis {axis} at index {slice_index}")

            # Create an interactive figure with Plotly using Heatmap
            fig = go.Figure(data=go.Heatmap(z=slice_2d, colorscale='viridis'))

            # Update layout to match image size
            fig.update_layout(
                xaxis=dict(title='X-axis', scaleanchor='x', constrain='domain'),
                yaxis=dict(title='Y-axis', scaleanchor='x'),
                xaxis_title="X",
                yaxis_title="Y",
                autosize=True,
                # width=slice_2d.shape[1],  # Adjust width based on image dimensions
                height=slice_2d.shape[0]  # Adjust height based on image dimensions
            )

            # Display the Plotly chart in Streamlit
            st.plotly_chart(fig)
        else:
            st.warning("No .npy files found in the specified folder.")
    else:
        st.error("The specified path is not a valid directory.")
else:
    st.info("Please enter a folder path or select the default folder.")
