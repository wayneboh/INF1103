FROM python:3.12-slim
WORKDIR /app
COPY inventory_manager.py inventory.py product.py physical_product.py digital_product.py can_be_shipped.py ./
CMD ["python", "inventory_manager.py"]