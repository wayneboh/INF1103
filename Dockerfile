FROM python:3.12-slim
WORKDIR /app
COPY inventory_manager.py inventory.py product.py physical_product.py digital_product.py can_be_shipped.py supplier.py order.py order_line.py discount_strategy.py no_discount.py percentage_discount.py bulk_discount.py student_discount.py product_factory.py products.csv ./
CMD ["python", "inventory_manager.py"]