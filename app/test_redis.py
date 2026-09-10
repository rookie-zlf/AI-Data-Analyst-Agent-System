from session_store import save_session,get_session,get_session_ttl,delete_session

session_data = {
    'file_path':'data/uploads/sales.csv',
    'messages':[
        {
            'role':'user',
            'content':'哪个商品单价最高?'
        },
        {
            'role':'assistant',
            'content':'macbook单价最高.'
        }
    ]
}


save_session('001',session_data)

session = get_session("001")


print(session)
print(type(session))
print('==========================================================')
session = delete_session("001")
print(session)


