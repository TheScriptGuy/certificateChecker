import datetime
from dateutil.relativedelta import relativedelta

from . import CertificateTimeFormat

class CertificateStatistics:
    """This class is responsible for helping with calculations of meta data."""
    CLASS_VERSION = "0.01"

    certificate_time_format = CertificateTimeFormat.CertificateTimeFormat().cert_time_format

    @staticmethod
    def returnNotAfter(__certificateObject) -> None:
        """Return the notAfter field from the certificate."""
        if __certificateObject is not None:
            return __certificateObject['notAfter']
        return ""

    @staticmethod
    def howMuchTimeLeft(__certificateObject) -> None:
        """Return the remaining time left on the certificate."""
        if __certificateObject is not None:
            timeNow = datetime.datetime.utcnow().replace(microsecond=0)
            certNotAfter = datetime.datetime.strptime(
                CertificateStatistics.returnNotAfter(
                    __certificateObject
                ),
                CertificateStatistics.certificate_time_format
            )

            __delta = relativedelta(certNotAfter, timeNow)

            myDeltaDate = {
                'years': __delta.years,
                'months': __delta.months,
                'days': __delta.days,
                'hours': __delta.hours,
                'minutes': __delta.minutes,
                'seconds': __delta.seconds,
            }
            timeLeft = []

            for field in myDeltaDate:
                if myDeltaDate[field] > 1:
                    timeLeft.append(f"{myDeltaDate[field]} {field}")
                else:
                    if myDeltaDate[field] == 1:
                        timeLeft.append(f"{myDeltaDate[field]} {field[:-1]}")

            certResult = ', '.join(timeLeft)
        else:
            certResult = "Invalid certificate"
        return certResult


