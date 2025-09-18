
import sys
import pytest
from io import StringIO

class Six:
    StringIO = StringIO

sys.modules['rdkit.six'] = Six()

if __name__ == '__main__':
    sys.exit(pytest.main())
