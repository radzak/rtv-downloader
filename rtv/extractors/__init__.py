from .ipla import Ipla
from .polsatnews import PolsatNews
from .polskieradio import PolskieRadio
from .radiozet import RadioZet
from .rmf24 import Rmf24
from .tokfm import TokFm
from .tvn24 import Tvn24
from .tvpinfo import TvpInfo
from .tvpparlament import TvpParlament
from .vod import Vod
from .vodtvp import VodTVP
from .wp import Wp

EXTRACTORS = [
    Ipla,
    PolsatNews,
    PolskieRadio,
    RadioZet,
    Rmf24,
    TokFm,
    Tvn24,
    TvpInfo,
    TvpParlament,
    Vod,
    VodTVP,
    Wp
]

__all__ = ['EXTRACTORS']
