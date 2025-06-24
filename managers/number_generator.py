from utils.mysql_helper import MySQLHelper
from models.number_generator import NumberGenerator
from repositorys.number_generator import NumberGeneratorRepository


class NumberGeneratorManager():
    def get(self, table_name: str, count: int):
        # db = MySQLHelper()
        # sql = 'select * from number_generator where table_name= %(table_name)s'
        # params = {'table_name': table_name}
        # table_number = db.single(sql, params)

        table_number = NumberGenerator.query.filter_by(table_name=table_name).first()
        table_number_dict = table_number.to_dict()
        if not table_number:
            # insert_sql = '''insert into number_generator(table_name, current_number)
            #                 values (%(table_name)s, %(current_number)s)'''
            # insert_params = {'table_name': table_name, 'current_number': count}
            # db.insert(insert_sql, insert_params)

            NumberGeneratorRepository.create(table_name=table_name, current_number=count)
            return 1
        else:
            # update_sql = '''update number_generator
            #                 set current_number = current_number + %(current_number)s
            #                 where table_name = %(table_name)s'''
            # update_params = {'table_name': table_name, 'current_number': count}
            # db.insert(update_sql, update_params)
            NumberGeneratorRepository.update({
                'table_name': table_name
            }, {
                NumberGenerator.current_number: NumberGenerator.current_number + count
            })
            return table_number_dict['current_number'] + 1
