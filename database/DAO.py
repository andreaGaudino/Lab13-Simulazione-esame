from database.DB_connect import DBConnect
from model.state import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(s.`datetime`) as data
                    from new_ufo_sightings.sighting s """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["data"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getForme(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.shape as forma
                    from new_ufo_sightings.sighting s 
                    where year(s.`datetime`) = %s
                    and s.shape != ""
                    order by s.shape
                     """

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(row["forma"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from state
                         """

        cursor.execute(query, ())

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi1():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select state1, state2
                    from neighbor
                    where state1<state2"""

        cursor.execute(query, ())

        for row in cursor:
            result.append([row["state1"], row["state2"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi2(forma, anno):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select upper(s2.state) as stato, count(distinct s2.id) as count
                from new_ufo_sightings.sighting s2 
                where s2.shape = %s
                and year(s2.`datetime`) = %s
                group by s2.state  """

        cursor.execute(query, (forma, anno))

        for row in cursor:
            result[row['stato']] = row["count"]

        cursor.close()
        conn.close()
        return result