import os


ENVS = dict()


def parse_env_variable(var_name, as_int=False, as_bool=False, default=None):
    global ENVS
    var = os.getenv(var_name)

    if var is None:
        if default is None:
            raise EnvironmentError(f'{var_name} is not defined!')
        return default

    if as_int or var_name.upper().endswith('_PORT'):
        var = int(var)
    if as_bool or var_name.upper().startswith('IS_'):
        var = var.upper() == 'TRUE'
    ENVS[var_name] = var
    return var


IP_ADDRESS = parse_env_variable('IP_ADDRESS', default='127.0.0.1')
PORT = parse_env_variable('PORT', as_int=True, default=8000)
DATABASE_URL = parse_env_variable('DATABASE_URL', default="sqlite+aiosqlite:///./test.db")
API_KEY = parse_env_variable('API_KEY')
