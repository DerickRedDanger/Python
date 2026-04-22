@dataclass(slots=True)
class SnapshotValue:
    captured: bool
    strategy: Optional[Literal["ref", "copy", "deepcopy"]]
    value: Any
    notes: List[Tuple[str, str, str]]

@dataclass(slots=True)
class SnapshotBundle:
    call_id: int

    origin: Literal["normal", "error"]

    args: SnapshotValue
    kwargs: SnapshotValue
    result: SnapshotValue

    has_result: bool