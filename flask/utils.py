class is_valid:

    def json(schema, document):

        # ha tobb mezo van a jsonban
        if len(schema.items()) < len(document.items()):
            return False

        for k, v in schema.items():
            if v['required']:  # ha a mezo required
                # ha a required mezo hianyzik
                if k not in document:
                    return False
        return True


class schemas:

    book_schema = {
        "flname": {
            "required": True
        },
        "lib_date": {
            "required": True
        },
        "pub_date": {
            "required": True
        },
        "publisher": {
            "required": True
        },
        "title": {
            "required": True
        }
    }


class get_books:

    def results(result):
        book = []
        for i in result:
            mydict = {
                'id': i.id,
                'author': i.author.flname,
                'title': i.title.title,
                'publisher': i.publisher.publisher,
                'pub_date': i.pub_date,
                'lib_date': i.lib_date,
                'created_at': i.created_at
            }
            book.append(mydict)

        return book
