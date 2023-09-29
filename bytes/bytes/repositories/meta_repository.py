from typing import Dict, List, Optional, Type
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from bytes.models import BoefjeMeta, MimeType, NormalizerMeta, RawData, RawDataMeta


class BoefjeMetaFilter(BaseModel):
    organization: str

    boefje_id: Optional[str] = None
    input_ooi: Optional[str] = "*"
    limit: int = 1
    offset: int = 0
    descending: bool = True


class NormalizerMetaFilter(BaseModel):
    organization: Optional[str] = None
    normalizer_id: Optional[str] = None
    raw_id: Optional[UUID] = None
    limit: int = 1
    offset: int = 0
    descending: bool = True


class RawDataFilter(BaseModel):
    organization: Optional[str] = None
    boefje_meta_id: Optional[UUID] = None
    normalized: Optional[bool] = None
    mime_types: List[MimeType] = Field(default_factory=list)
    limit: int = 1
    offset: int = 0

    @model_validator(mode="after")
    def either_organization_or_boefje_meta_id(self):
        if self.organization or self.boefje_meta_id:
            return self

        raise ValueError("boefje_meta_id and organization cannot both be None.")


class MetaDataRepository:
    def __enter__(self) -> None:
        pass

    def __exit__(self, _exc_type: Type[Exception], _exc_value: str, _exc_traceback: str) -> None:
        pass

    def save_boefje_meta(self, boefje_meta: BoefjeMeta) -> None:
        raise NotImplementedError()

    def get_boefje_meta_by_id(self, boefje_meta_id: UUID) -> BoefjeMeta:
        raise NotImplementedError()

    def get_boefje_meta(self, query_filter: BoefjeMetaFilter) -> List[BoefjeMeta]:
        raise NotImplementedError()

    def save_normalizer_meta(self, normalizer_meta: NormalizerMeta) -> None:
        raise NotImplementedError()

    def get_normalizer_meta_by_id(self, normalizer_meta_id: UUID) -> NormalizerMeta:
        raise NotImplementedError()

    def get_normalizer_meta(self, query_filter: NormalizerMetaFilter) -> List[NormalizerMeta]:
        raise NotImplementedError()

    def save_raw(self, raw: RawData) -> UUID:
        raise NotImplementedError()

    def get_raw_by_id(self, raw_id: UUID) -> RawData:
        raise NotImplementedError()

    def get_raw(self, query_filter: RawDataFilter) -> List[RawDataMeta]:
        raise NotImplementedError()

    def has_raw(self, boefje_meta: BoefjeMeta, mime_types: List[MimeType]) -> bool:
        raise NotImplementedError()

    def get_raw_file_count_per_organization(self) -> Dict[str, int]:
        raise NotImplementedError()
