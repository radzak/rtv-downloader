from .polskieradio import PolskieRadio
from .tokfm import TokFm
from .radiozet import RadioZet
from .vodtvp import VodTVP
from .polsatnews import PolsatNews
from .vod import Vod
from .ipla import Ipla
from .rmf24 import Rmf24
from .tvn24 import Tvn24
from .tvpparlament import TvpParlament
from .tvpinfo import TvpInfo


EXTRACTORS = [
    PolskieRadio,
    TokFm,
    RadioZet,
    VodTVP,
    PolsatNews,
    Vod,
    Ipla,
    Rmf24,
    Tvn24,
    TvpParlament,
    TvpInfo
    ]


__all__ = ['EXTRACTORS']
