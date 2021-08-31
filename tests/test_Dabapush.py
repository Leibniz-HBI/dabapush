from pytest import fixture, skip
from pathlib import Path
from dabapush.Dabapush import Dabapush

@fixture
def dabapush():
    return Dabapush()

# should be a Singleton (DONE)
def test_singleton(dabapush):
    assert dabapush == Dabapush()
# should be a Interface?
# should 
# should accept ProjectConfiguration and Configuration 
# should accept a working directory
def test_working_directory(dabapush):
    assert dabapush.working_dir == Path()
# should accept a installation directory (or a directory for a global conf)
# should dispatch changes in the configuration
# should acquire targets
# should dispatch jobs
# should update targets per jop
# should persistently keep state for targets and jobs

