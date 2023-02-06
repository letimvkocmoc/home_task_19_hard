from dao.model.genre import Genre
from config import Config

class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Genre).get(bid)

    def get_all(self, filter):
        page = filter.get('page')
        if page is not None:
            result = self.session.query(Genre).paginate(int(page), Config.ITEMS_PER_PAGE, max_per_page=Config.MAX_PAGE,
                                                        error_out=False).items
            return result
        else:
            return self.session.query(Genre).all()

    def create(self, genre_d):
        ent = Genre(**genre_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        genre = self.get_one(rid)
        self.session.delete(genre)
        self.session.commit()

    def update(self, genre_d):
        genre = self.get_one(genre_d.get("id"))
        genre.name = genre_d.get("name")

        self.session.add(genre)
        self.session.commit()
