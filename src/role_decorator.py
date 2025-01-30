from functools import wraps

current_user_role = None

def set_current_user_role(role):
    global current_user_role
    current_user_role = role

def access_control(*, roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if current_user_role not in roles:
                raise PermissionError(f"Доступ запрещен для роли '{current_user_role}'. "
                                      f"Допустимые роли: {roles}.")
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@access_control(roles=['admin', 'moderator'])
def restricted_function():
    return "Access granted to restricted function."

if __name__ == "__main__":
    try:
        set_current_user_role('user')
        print(restricted_function())
    except PermissionError as e:
        print(e)

    set_current_user_role('admin')
    print(restricted_function())