from bitrix_service import BitrixService


def run_etl():
    bitrix_service = BitrixService()
    bitrix_service.get_code()
    # bitrix_service.auth()
    # users = bitrix_service.get_users()
    # return users
    # users = get_users(bitrix_service.access_token)
    # return users

if __name__ == '__main__':
    run_etl()
