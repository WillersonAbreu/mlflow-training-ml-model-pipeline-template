from contextlib import ContextDecorator
import os
import sys

class PathLoadContext(ContextDecorator):
    def __enter__(self):
        # Adicionando diretório src no path do python para importar o módulo utils
        current = os.getcwd()
        parent = os.path.join(current, 'src')
        
        sys.path.insert(0, os.path.dirname(current))        
        sys.path.insert(0, os.path.dirname(parent))
        return self
    
    def __exit__(self, *exc):
        return False