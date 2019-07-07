def insert_seeds(db, fn, objs):
    for obj in objs:
        db.session.add(fn(obj))
