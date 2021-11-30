from pytest import fixture, skip
from pathlib import Path
from dabapush.Dabapush import Dabapush

@fixture
def dabapush():
    return Dabapush()

# should be a Singleton (DONE)
def test_singleton(dabapush):
    assert dabapush == Dabapush()

# should accept a working directory
def test_working_directory(dabapush):
    assert dabapush.working_dir == Path()

# should accept a installation directory (or a directory for a global conf)
def test_install_directory(dabapush: Dabapush):
    skip()
# should dispatch changes in the configuration
def test_conf_dispatch(dabapush: Dabapush):
    skip()
# should acquire targets
def test_acquire_targets(dabapush: Dabapush):
    skip()
# should persistently keep state for targets and jobs
def test_persist_state(dabapush: Dabapush):
    skip()
# should initilize a project configuration
def test_initiliaze(dabapush: Dabapush, tmpdir: Path):
    dabapush.working_dir = tmpdir
    dabapush.pr_init()
    assert True
# should write a project configration
def test_write_conf(dabapush: Dabapush):
    skip()
# should read a project configuration
def test_read_conf(dabapush: Dabapush):
    skip()
# should add a reader and give it a name/id
def test_add_reader(dabapush: Dabapush):
    skip()
# should update readers by name/id
def test_update_reader(dabapush: Dabapush):
    skip()
# should remove a reader by name/id
def test_rm_reader(dabapush: Dabapush):
    skip()
# should add a writer and give it a name/id
def test_add_writer(dabapush: Dabapush):
    skip()
# should update writers by name/id
def test_writer_update(dabapush: Dabapush):
    skip()
# should remove a writer by name/id
def test_rm_writer(dabapush: Dabapush):
    skip()
# should run a job
def test_run_job(dabapush: Dabapush):
    skip()
# should update the jobs targets
def test_update_job(dabapush: Dabapush):
    skip()
