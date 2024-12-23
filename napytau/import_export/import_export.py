from pathlib import PurePath
from re import compile as compile_regex
from typing import Optional, List

from napytau.import_export.factory.napatau.napatau_factory import (
    NapatauFactory,
)
from napytau.import_export.factory.napatau.raw_napatau_data import RawNapatauData
from napytau.import_export.crawler.file_crawler import FileCrawler
from napytau.import_export.crawler.napatau_setup_files import NapatauSetupFiles
from napytau.import_export.factory.napatau.raw_napatau_setup_data import (
    RawNapatauSetupData,
)
from napytau.import_export.model.dataset import DataSet
from napytau.import_export.reader.file_reader import FileReader

IMPORT_FORMAT_NAPATAU = "napatau"

IMPORT_FORMATS = [IMPORT_FORMAT_NAPATAU]


def import_napatau_format_from_files(
    directory_path: PurePath, fit_file_path: Optional[PurePath] = None
) -> List[DataSet]:
    """
    Ingests a dataset from the Napatau format. The directory path will be
    recursively searched for the following files:
    - v_c
    - distances.dat
    - norm.fac
    - optional: *.fit

    if the fit_file_path is provided, the fit file will be
    read from this path instead of the directory.
    """

    file_crawler = _configure_file_crawler(fit_file_path)

    setup_file_bundles: List[NapatauSetupFiles] = file_crawler.crawl(directory_path)

    return list(
        map(
            lambda setup_files: NapatauFactory.create_dataset(
                RawNapatauData(
                    FileReader.read_rows(setup_files.velocity_file),
                    FileReader.read_rows(setup_files.distances_file),
                    FileReader.read_rows(setup_files.fit_file),
                    FileReader.read_rows(setup_files.calibration_file),
                )
            ),
            setup_file_bundles,
        )
    )


def _configure_file_crawler(fit_file_path: Optional[PurePath]) -> FileCrawler:
    if fit_file_path:
        file_crawler = FileCrawler(
            [
                compile_regex("v_c"),
                compile_regex("distances.dat"),
                compile_regex("norm.fac"),
            ],
            lambda files: NapatauSetupFiles.create_from_file_names(
                files + [fit_file_path]
            ),
        )

    else:
        file_crawler = FileCrawler(
            [
                compile_regex("v_c"),
                compile_regex("distances.dat"),
                compile_regex("norm.fac"),
                compile_regex(".*.fit"),
            ],
            lambda files: NapatauSetupFiles.create_from_file_names(files),
        )
    return file_crawler


def read_napatau_setup_data_into_data_set(
    dataset: DataSet, setup_file_path: PurePath
) -> DataSet:
    """
    Reads the setup data from the provided file path and adds it to the provided dataset
    """

    setup_data = FileReader.read_rows(setup_file_path)

    return NapatauFactory.enrich_dataset(dataset, RawNapatauSetupData(setup_data))
