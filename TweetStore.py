import couchdb
import couchdb.design


COUCH_SERVER = 'http://192.168.1.106:5984/'

class TweetStore:
        def __init__(self, dbname, url=None):
            self.server = couchdb.Server(url=url)
            try:
                self.db = self.server[dbname]
            except:
                self.db = self.server.create(dbname)
                self._create_views()

        def create_db(self, name):
            try:
                self.db = self.server.create(name)
                self._create_views()
            except couchdb.http.PreconditionFailed:
                self.db = self.server[dbname]

        def _create_views(self):
            count_map = 'function(doc) { emit(doc.id, 1); }'
            count_reduce = 'function(keys, values) { return sum(values); }'
            view = couchdb.design.ViewDefinition('twitter', 'count_tweets', count_map, reduce_fun=count_reduce)
            view.sync(self.db)

            get_tweets = 'function(doc) { emit(("0000000000000000000"+doc.id).slice(-19), doc); }'
            view = couchdb.design.ViewDefinition('twitter', 'get_tweets', get_tweets)
            view.sync(self.db)


        def save_tweet(self, tw):
            tw['_id'] = tw['id_str']
            self.db.save(tw)

        def count_tweets(self):
            for doc in self.db.view('twitter/count_tweets'):
                return doc.value

        def get_tweets(self):
            return [doc.doc for doc in self.db.iterview('_all_docs', batch=50, \
                    include_docs=True)]


