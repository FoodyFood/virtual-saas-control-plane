billing_entities: list[dict[str, str, str]] = [] # tenant_id, billing_address


class BillingManagement():
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

    def delete_billing_entity(self, tenant_id: str = None) -> str:
        for billing_entity in billing_entities:
            if billing_entity[0] == tenant_id:
                billing_entities.remove(billing_entity)
        return True
