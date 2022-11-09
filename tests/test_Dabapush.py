# pylint: disable=W0621
from pathlib import Path

import yaml
from pytest import fixture, mark, skip

from dabapush.Dabapush import Dabapush


@fixture
def dabapush():
    """Provides a Dabapush-instance."""
    return Dabapush()


def test_singleton(dabapush):
    """Should be a Singleton."""
    assert dabapush == Dabapush()


def test_working_directory(dabapush):
    """should accept a working directory."""
    assert dabapush.working_dir == Path().resolve()


def test_install_directory():
    """Should accept a installation directory (or a directory for a global conf)."""
    skip()


def test_conf_dispatch():
    """Should dispatch changes in the configuration."""
    skip()


def test_project_configuration_write(dabapush: Dabapush, tmpdir: Path):
    """Should persistently keep state for targets and jobs."""
    dabapush.working_dir = tmpdir
    dabapush.pr_write()
    test_path = dabapush.working_dir / "dabapush.yml"
    with test_path.open("r") as file:
        conf = yaml.full_load(file)
    assert test_path.exists()
    assert conf


def test_initialize(dabapush: Dabapush, tmpdir: Path):
    """Should initialize a project configuration."""
    dabapush.working_dir = tmpdir
    dabapush.pr_init()
    dabapush.pr_write()
    test_path = tmpdir / "dabapush.yml"
    assert test_path.exists()


def test_write_conf(dabapush: Dabapush, tmpdir: Path):
    """Should write a project configration."""
    dabapush.working_dir = tmpdir
    dabapush.pr_init()
    dabapush.rd_add("Twacapic", "default")
    dabapush.pr_write()
    test_path = Path(tmpdir) / "dabapush.yml"
    with test_path.open("r") as file:
        candidate = yaml.full_load(file)
    assert dabapush.config.name == candidate.name


@mark.parametrize("reader,name", [("Twacapic", "reader1")])
def test_add_reader(tmpdir: Path, reader: str, name: str):
    """Should add a reader and give it a name/id."""
    dabapush = Dabapush(working_dir=tmpdir)
    dabapush.rd_add(reader, name)
    assert name in dabapush.config.readers


def test_update_reader():
    """Should update readers by name/id."""
    skip()


def test_rm_reader():
    """Should remove a reader by name/id."""
    skip()


def test_add_writer():
    """Should add a writer and give it a name/id."""
    skip()


def test_writer_update():
    """Should update writers by name/id."""
    skip()


def test_rm_writer():
    """Should remove a writer by name/id."""
    skip()


def test_run_job():
    """Should run a job."""
    skip()


def test_update_job():
    """Should update the jobs targets."""
    skip()
