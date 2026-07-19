from prometheus_client import Counter

# Business metric scraped by the payments-monitoring-lab project.
invoices_paid_total = Counter("invoices_paid_total", "Number of invoices successfully paid")
