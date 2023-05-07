from services.MetricsManagement import MetricsManagement


# Fake database
billing_entities: list[dict[str, str, str]] = [] # tenant_id, billing_address


class BillingManagement():
    _metrics_management: MetricsManagement = MetricsManagement()
    
    def create_billing_entity(self, tenant_id: str = None, billing_address: str = None) -> str:
        for billing_entity in billing_entities:
            if billing_entity == [tenant_id, billing_address]:
                return True # Entity already exists

        billing_entities.append([tenant_id, billing_address])
        return True

    def get_billing_entity_for_tenant(self, tenant_id: str):
        for billing_entity in billing_entities:
            if billing_entity[0] == tenant_id:
                return (billing_entity)

    def generate_invoice(self, tenant_id: str = None):
        tenant_metrics = self._metrics_management.get_metrics_for_tenant(tenant_id=tenant_id)
        # Multiply your metrics by some cost here per metric/usage
        invoice_line_items = tenant_metrics
        return invoice_line_items

    def delete_billing_entity(self, tenant_id: str = None) -> str:
        for billing_entity in billing_entities:
            if billing_entity[0] == tenant_id:
                billing_entities.remove(billing_entity)
        return True
