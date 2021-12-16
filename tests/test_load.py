import hupavddb
from translate import Translator

translator = Translator(to_lang="en", from_lang="es")

dbdir = r"C:\Users\Takeshi Ikuma\OneDrive - LSUHSC\data\BDAtos HUPA Segmentada"

hupavddb.load_db(dbdir)
print([translator.translate(t) for t in hupavddb.get_fields()])
