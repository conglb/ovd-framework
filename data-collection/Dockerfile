FROM python:3.9

# set working directory
WORKDIR /app

# install packages
RUN pip install --no-cache-dir streamlit pandas requests flask streamlit_monaco schedule

# Expose 8511 for Streamlit, 8011 for API
EXPOSE 8011
EXPOSE 8511

# Run Streamlit
CMD ["streamlit", "run", "Module_Management.py", "--server.port=8511"]