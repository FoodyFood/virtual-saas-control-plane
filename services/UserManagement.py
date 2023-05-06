# Fake databases
users:  list[dict[str, str, str]] = []  # email, customer_shortname, tenant_id


class UserManagement():
    def create_user(self, email: str = None, customer_shortname: str = None, tenant_id: str = None) -> bool:
        if (email == None or customer_shortname == None or tenant_id == None):
            return None

        # Check if the user already exists in the database
        for user in users:
            if (user[0] == email and user[1] == customer_shortname and user[2] == tenant_id):
                return True  # User already exists

        # Add the user to the users database
        users.append([email, customer_shortname, tenant_id])
        return True

    def get_users_for_tenant(self, tenant_id: str = None):
        if (tenant_id == None):
            return None

        list_of_users_for_tenant: list[dict[str, str, str]] = []

        for user in users:
            if (user[2] == tenant_id):
                list_of_users_for_tenant.append(user)

        return (list_of_users_for_tenant)

    def delete_user(self, user) -> bool:
        if (user == None):
            return None

        users.remove(user)
        return True
