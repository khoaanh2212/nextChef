from south.db import db as connection
import logging

def run_sql_file(file, db = connection):

    logging.info("opening %s" % file)

    with open(file) as f:
        sql = unicode(f.read(), 'utf-8')

        logging.info('executing %s' % file)

        for line, query in enumerate(sql.split("\n")):
            if not query.strip():
                continue
            try:
                db.execute(query)
            except Exception as e:
                logging.error("Wrong query in file %s at line %d:\n" % (file, line))
                logging.debug(query)
                raise e
