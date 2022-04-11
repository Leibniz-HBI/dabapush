import yaml
from typing import ChainMap, Dict, List
from importlib import import_module
from loguru import logger as log
from .ReaderConfiguration import ReaderConfiguration
from .WriterConfiguration import WriterConfiguration


class Registry(yaml.YAMLObject):
    """ """

    yaml_tag = "!dabapush:Registry"

    _instances = []

    """ """

    def __new__(cls):
        t = super(Registry, cls).__new__(cls)
        Registry._instances.append(t)

        return t

    def __init__(
        self, readers: Dict[str, str] = {}, writers: Dict[str, str] = {}
    ) -> None:
        super().__init__()

        self.readers = readers
        self.writers = writers

    def __del__(self):
        Registry._instances.remove(self)

    def __repr__(self) -> str:
        return super().__repr__()

    # --- static methods --- #

    @staticmethod
    def get_reader(type: str) -> ReaderConfiguration or None:
        """

        Parameters
        ----------
        type :
            str: registry key
            Returns: ReaderConfiguration or None: the requested ReaderConfiguration or None if
            no matching configuration is found.
        type :
            str:
        type :
            str:
        type: str :


        Returns
        -------

        """
        a: list[ReaderConfiguration] = [inst.readers for inst in Registry._instances]
        readers = ChainMap(*a)

        if type in readers:
            instance_info = readers[type]
            log.debug(
                f'Creating Configuration instance from {", ".join(instance_info)}.'
            )
            reader_configuration = import_module(
                instance_info["moduleName"], package="dabapush"
            ).__getattribute__(instance_info["className"])

            return reader_configuration

    @staticmethod
    def get_writer(type: str) -> WriterConfiguration or None:
        """

        Parameters
        ----------
        type :
            str:
        type :
            str:
        type :
            str:
        type: str :


        Returns
        -------

        """
        a = [inst.writers for inst in Registry._instances]
        writers = ChainMap(*a)

        if type in writers:
            instance_info = writers[type]
            log.debug(
                f'Creating Configuration instance from {", ".join(instance_info)}.'
            )
            writer_configuration = import_module(
                instance_info["moduleName"], package="dabapush"
            ).__getattribute__(instance_info["className"])

            return writer_configuration

    @staticmethod
    def __ensure_reader__(arg: any) -> bool:
        # TODO: this is a stub function, which _should_ ensure that
        # things passed in here are actually ReaderConfigurations _OR_
        # classes that inherit from that.
        return issubclass(arg, ReaderConfiguration)

    @staticmethod
    def __ensure_writer__(arg: any) -> bool:
        # TODO: this is a stub function, which _should_ ensure that
        # things passed in here are actually WriterConfigurations _OR_
        # classes that inherit from that.
        return issubclass(arg, WriterConfiguration)

    @staticmethod
    def list_all_readers() -> List[str]:
        """ """
        a = [inst.readers for inst in Registry._instances]
        readers = ChainMap(*a)
        return [i for i in readers]

    @staticmethod
    def list_all_writers() -> List[str]:
        """ """
        a = [inst.writers for inst in Registry._instances]
        writers = ChainMap(*a)
        return [i for i in writers]

    # --- instance methods --- #
    def register_reader(self, name: str, plugin_configuration) -> None:
        """

        Parameters
        ----------
        name :
            str:
        constructor :
            param name: str:
        plugin_configuration :
            param name: str:
        name: str :


        Returns
        -------

        """
        if Registry.__ensure_reader__(plugin_configuration):
            self.readers[name] = plugin_configuration

    def register_writer(self, name: str, constructor) -> None:
        """

        Parameters
        ----------
        name :
            str:
        constructor :
            param name: str:
        name :
            str:
        name: str :


        Returns
        -------

        """
        pass

    def remove_reader(self, name: str) -> bool:
        """

        Parameters
        ----------
        name :
            str:
        name :
            str:
        name :
            str:
        name: str :


        Returns
        -------

        """
        pass

    def remove_writer(self, name: str) -> bool:
        """

        Parameters
        ----------
        name :
            str:
        name :
            str:
        name :
            str:
        name: str :


        Returns
        -------

        """
        pass

    def list_writers(self) -> List[str]:
        """ """
        pass

    def list_writers(self) -> List[str]:
        """ """
        pass
