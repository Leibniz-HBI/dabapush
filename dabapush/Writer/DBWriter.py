from sqlalchemy import create_engine
import io
from .Writer import Writer


class DBWriter(Writer):

    def __init__(self):
        super().__init__()

    def persist(self, chunkSize: int):

        engine = create_engine('postgresql+psycopg2://username:password@host:port/database')
        df = self.buffer.head(chunkSize)

        df.head(0).to_sql('table_name', engine, if_exists='fail',index=False) #drops old table and creates new empty table

        conn = engine.raw_connection()
        cur = conn.cursor()
        output = io.StringIO()
        df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        contents = output.getvalue()
        cur.copy_from(contents, 'table_name', null="") # null values become ''
        conn.commit()