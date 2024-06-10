# Use the official Jupyter base image
FROM quay.io/jupyter/base-notebook

# Install pymongo and mongoengine
RUN pip install pymongo mongoengine

# Expose port for Jupyter Lab
EXPOSE 8888

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
