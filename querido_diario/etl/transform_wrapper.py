exit()
ipython
from querido_diario.etl.transform_files import get_text_from_file
TIKA_PATH = '/usr/local/Cellar/tika/1.24.1_1/libexec/tika-app-1.24.1.jar'
import sys
with open ('/dev/null', 'w') as f:
    file = get_text_from_file('scratch/arquivo_teste.pdf', TIKA_PATH)
