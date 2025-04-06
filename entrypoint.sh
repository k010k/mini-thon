#!/bin/bash

# Start the MCP server in the background
python mcp_server_remote.py &

# Run the Streamlit application
streamlit run app_Docker.py --server.port=8501 --server.enableCORS=false