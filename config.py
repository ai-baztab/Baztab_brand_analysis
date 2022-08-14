date_from_id = 'history-from'
date_to_id = 'history-to'
price_list_id = 'table-list'
table_name = 'dollar'
btn_next = 'DataTables_Table_0_next'
btns_id = 'DataTables_Table_0_paginate'
create_command = '''
OPEN float NOT NULL,
 LOW float NOT NULL,
  HIGH float NOT NULL,
   CLOSE float NOT NULL,
    DateE DATE NOT NULL PRIMARY KEY, 
    DateF CHAR(10) NOT NULL
    '''
price_keywords = ['OPEN', 'LOW', 'HIGH', 'CLOSE']