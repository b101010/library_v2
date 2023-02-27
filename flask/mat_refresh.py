import psycopg

class mat:

    def refresh():

        db = psycopg.connect(
            dbname = "library",
            host ="postgres",
            user ="postgres",
            password ="valami",
        )

        cur = db.cursor()
        sql = 'REFRESH MATERIALIZED VIEW CONCURRENTLY public.avg_age WITH DATA'
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = 'REFRESH MATERIALIZED VIEW CONCURRENTLY public.avg_pub_to_lib_stat WITH DATA'
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = 'REFRESH MATERIALIZED VIEW CONCURRENTLY public.dist_books_authors WITH DATA'
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = 'REFRESH MATERIALIZED VIEW CONCURRENTLY public.max_age WITH DATA'
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = 'REFRESH MATERIALIZED VIEW CONCURRENTLY public.min_age WITH DATA'
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = 'REFRESH MATERIALIZED VIEW CONCURRENTLY public.sum_books_authors WITH DATA'
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = 'REFRESH MATERIALIZED VIEW CONCURRENTLY public.t_stat WITH DATA'
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = 'REFRESH MATERIALIZED VIEW CONCURRENTLY public.ta_stat WITH DATA'
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = 'REFRESH MATERIALIZED VIEW CONCURRENTLY public.younger_than_avg WITH DATA'
        cur.execute(sql)
        db.commit()

        db.close()          