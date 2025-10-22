import sys
from pathlib import Path

from tests.unit.fixtures import *

conftest_dir = Path(__file__).resolve()
module_name: str = "ccc"
module_path: Path | None = next(
    (parent for parent in conftest_dir.parents if Path(parent / module_name).is_dir()),
    None,
)
if not module_path:
    raise Exception(f"{module_name} dir not found in parents")


sys.path.append(str(module_path))
