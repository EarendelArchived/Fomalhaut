from datetime import datetime as _datetime
from datetime import timedelta as _timedelta
from datetime import timezone as _timezone

from ..core import Enum as _Enum


class Timezone(_Enum):
    """
    Datetime 객체에 적용할 시간대를 정의합니다.
    """
    KST = 9

    def apply(self, target: _datetime) -> _datetime:
        """
        Datetime 객체에 시간대를 적용합니다.

        Parameters
        ----------
        target: datetime
            시간대를 적용할 Datetime 객체
        """
        return target.astimezone(_timezone(_timedelta(hours=self.value)))


def strfdelta(timedelta: _timedelta) -> str:
    """
    timedelta 객체를 문자열로 변환합니다.

    Parameters
    ----------
    timedelta: timedelta
        timedelta 객체
    """
    d = {"days": timedelta.days}
    d["hours"], rem = divmod(timedelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    value: str = "{days}일 {hours}시간 {minutes}분 {seconds}초".format(**d)
    if d["days"] == 0:
        return value.split("일 ")[1]
    return value


def calculateable_with_iso(datetime: _datetime) -> _datetime:
    """
    datetime 객체를 ISO 포맷과 함께 계산할 수 있도록 만듭니다.

    Parameters
    ----------
    datetime: datetime
        datetime 객체
    """
    return _datetime.fromisoformat(datetime.isoformat().split(".")[0] + "Z")
