# Fake database
users:  list[dict[str, str]] = []  # tenant_id, email


class IdentityManagement():
    '''
    Typically handled by something like cognito or octa
    Identity tool chosen must handle jwt claims so it can store the tenant_id
    '''

    def add_user(self, tenant_id: str = None, email: str = None) -> bool:
        for user in users:
            if user[1] == email:
                return True
        users.append([tenant_id, email])
        return True

    def user_sign_in(email: str = None, password: str = None):
        print("Fake sign in function that would typically handle the user signing in and return a token")
        for user in users:
            if user[1] == email:
                return (f"JWT with tenant_id embedded, tenant_id of user: {user[0]}")

    def get_list_of_users(self):
        return (users)
    
    def delete_user(self, user: dict[str, str] = None) -> bool:
        users.remove(user)
        return True