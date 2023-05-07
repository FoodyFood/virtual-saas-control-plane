class MetricsManagement():
    def get_metrics_for_tenant(self, tenant_id: str = None):
        # Here we should look up some database with the usage metrics of the tenant and return them
        return ([["compute", 15], ["memory", 3], ["apis", 25]])
