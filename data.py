import psycopg2
from psycopg2.extensions import AsIs



class Database():
    def __init__(self,dbname,username,password):

        self.__conection= psycopg2.connect("dbname={0} user={1} password={2}".format(dbname,username,password))
        self.cur = self.__conection.cursor()
        self.__conection.autocommit = False


    def add_element(self,tablename,request_dict):
        request_dict = dict(request_dict)
        columns = request_dict.keys()

        values = [request_dict[column] for column in columns]

        insert_statement = "insert into {0} (%s) values %s".format(tablename)
        insert_statement = self.cur.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
        insert_statement = str(insert_statement)[2:-1]
        try:
            self.cur.execute(insert_statement)
            self.__conection.commit()
        except (Exception, psycopg2.IntegrityError, psycopg2.DatabaseError) as e:
            self.__conection.rollback()
            raise e

    def select_all_element_from_columns(self, tablename, columns):

        select_statement = "SELECT %s FROM {0} ".format(tablename)

        select_statement = self.cur.mogrify(select_statement, (AsIs(','.join(columns)),))
        select_statement = str(select_statement)[2:-1]

        self.cur.execute(select_statement)
        print(self.cur.fetchall())

    def select_route_by_name(self, rout_name,**kwargs):

        self.cur.execute("SELECT * FROM route WHERE rname= %s", (rout_name,))
        result=self.cur.fetchall()
        if result:
            return result
        else:
            return []


    def authentication(self,login,parol):
        self.cur.execute("SELECT id FROM user_information WHERE login=%s AND parol= %s",(login,parol))

        if self.cur.fetchall() :
            return True
        else:
            return False




try:
    db=Database('postgres','postgres','1111')
except psycopg2.OperationalError:
    print("Not connected")
#d={"name" :'nemo',"email":"nemo222@gmail.com","login":"nemo","parol":'1111'}
#db.add_element("user_information",d)

