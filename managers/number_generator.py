from utils.mysql_helper import MySQLHelper


class NumberGenerator():
    def get(self, table_name: str, count: int):
        db = MySQLHelper()
        sql = 'select * from number_generator where table_name= %(table_name)s'
        params = {'table_name': table_name}
        table_number = db.single(sql, params)
        if not table_number:
            insert_sql = '''insert into number_generator(table_name, current_number)
                            values (%(table_name)s, %(current_number)s)'''
            insert_params = {'table_name': table_name, 'current_number': count}
            db.insert(insert_sql, insert_params)
            return 1
        else:
            update_sql = '''update number_generator
                            set current_number = current_number + %(current_number)s
                            where table_name = %(table_name)s'''
            update_params = {'table_name': table_name, 'current_number': count}
            db.insert(update_sql, update_params)
            return table_number['current_number'] + 1
