import os
from pprint import pprint


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("main/admin.py")))

pprint("main/admin.py")
pprint(os.path.abspath("main/admin.py"))
pprint(os.path.dirname(os.path.abspath("main/admin.py")))
pprint(BASE_DIR)
