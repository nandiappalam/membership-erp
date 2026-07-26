import qrcode
from django.conf import settings
import os


def generate_agm_qr(event):

    url = (
        "https://your-domain.com"
        "/events/agm-entry/"
        + str(event.id)
        + "/"
    )


    img = qrcode.make(url)


    filename = (
        "agm_entry_"
        + str(event.id)
        + ".png"
    )


    path = os.path.join(
        settings.MEDIA_ROOT,
        "event_qr",
        filename
    )


    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )


    img.save(path)


    return (
        settings.MEDIA_URL
        + "event_qr/"
        + filename
    )