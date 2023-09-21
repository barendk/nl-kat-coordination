from typing import List, Tuple, Union

from boefjes.job_models import BoefjeMeta


def run(boefje_meta: BoefjeMeta) -> List[Tuple[set, Union[bytes, str]]]:
    raise RuntimeError("This boefje is container-native")
