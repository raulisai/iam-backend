import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "iam_backend")

class DBResult:
    def __init__(self, data, error=None):
        self.data = data
        self.error = error

class LocalDBClient:
    def __init__(self, table_name=None):
        self.table_name = table_name
        self.query_type = None
        self.select_columns = "*"
        self.data_payload = None
        self.filters = []
        self.order_by = None
        self.limit_val = None

    def from_(self, table_name):
        return LocalDBClient(table_name)

    def select(self, columns='*'):
        self.query_type = 'SELECT'
        self.select_columns = columns
        return self

    def insert(self, data):
        self.query_type = 'INSERT'
        self.data_payload = data
        return self

    def update(self, data):
        self.query_type = 'UPDATE'
        self.data_payload = data
        return self

    def delete(self):
        self.query_type = 'DELETE'
        return self

    def eq(self, column, value):
        self.filters.append((column, '=', value))
        return self

    def gte(self, column, value):
        self.filters.append((column, '>=', value))
        return self
    
    def lte(self, column, value):
        self.filters.append((column, '<=', value))
        return self

    def in_(self, column, values):
        if values:
            self.filters.append((column, 'IN', tuple(values)))
        return self

    def order(self, column, desc=False):
        direction = 'DESC' if desc else 'ASC'
        self.order_by = f"{column} {direction}"
        return self

    def limit(self, count):
        self.limit_val = count
        return self

    def execute(self):
        conn = None
        try:
            conn = psycopg2.connect(
                host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            sql = ""
            params = []
            
            if self.query_type == 'SELECT':
                # Quick fix for the *, task_templates(*) syntax
                # We will just ignore the join request here and return flat data, 
                # relying on service refactoring to handle the relationships.
                # If select_columns contains '(*)', we default to '*' to prevent SQL errors
                cols = self.select_columns
                if '(*)' in cols:
                    cols = '*' 
                
                sql = f"SELECT {cols} FROM {self.table_name}"
                if self.filters:
                    where_clauses = []
                    for col, op, val in self.filters:
                        where_clauses.append(f"{col} {op} %s")
                        params.append(val)
                    sql += " WHERE " + " AND ".join(where_clauses)
                
                if self.order_by:
                    sql += f" ORDER BY {self.order_by}"
                
                if self.limit_val:
                    sql += f" LIMIT {self.limit_val}"
                    
                cur.execute(sql, tuple(params))
                data = cur.fetchall()
                # Convert RealDictRow to dict
                data = [dict(row) for row in data]
                return DBResult(data)

            elif self.query_type == 'INSERT':
                keys = self.data_payload.keys()
                cols = ", ".join(keys)
                placeholders = ", ".join(["%s"] * len(keys))
                sql = f"INSERT INTO {self.table_name} ({cols}) VALUES ({placeholders}) RETURNING *"
                
                vals = list(self.data_payload.values())
                cur.execute(sql, tuple(vals))
                conn.commit()
                data = cur.fetchall()
                data = [dict(row) for row in data]
                return DBResult(data)

            elif self.query_type == 'UPDATE':
                set_clauses = []
                for key in self.data_payload.keys():
                    set_clauses.append(f"{key} = %s")
                
                sql = f"UPDATE {self.table_name} SET {', '.join(set_clauses)}"
                params = list(self.data_payload.values())
                
                if self.filters:
                    where_clauses = []
                    for col, op, val in self.filters:
                        where_clauses.append(f"{col} {op} %s")
                        params.append(val)
                    sql += " WHERE " + " AND ".join(where_clauses)
                
                sql += " RETURNING *"
                cur.execute(sql, tuple(params))
                conn.commit()
                data = cur.fetchall()
                data = [dict(row) for row in data]
                return DBResult(data)

            elif self.query_type == 'DELETE':
                sql = f"DELETE FROM {self.table_name}"
                if self.filters:
                    where_clauses = []
                    for col, op, val in self.filters:
                        where_clauses.append(f"{col} {op} %s")
                        params.append(val)
                    sql += " WHERE " + " AND ".join(where_clauses)
                
                sql += " RETURNING *"
                cur.execute(sql, tuple(params))
                conn.commit()
                data = cur.fetchall()
                data = [dict(row) for row in data]
                return DBResult(data)
                
        except Exception as e:
            print(f"DB Error: {e}")
            return DBResult(None, str(e))
        finally:
            if conn:
                conn.close()

def get_supabase():
    # Return an object that has a from_ method
    return LocalDBClient()
