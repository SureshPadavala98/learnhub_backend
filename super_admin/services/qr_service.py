import os

import qrcode

from django.conf import settings
from django.core.files import File


class QRCodeService:

    @staticmethod
    def generate(certificate):

        verify_url = (
            f"https://stepupmark.com/verify/"
            f"{certificate.certificate_id}"
        )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(verify_url)

        qr.make(fit=True)

        image = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        filename = (
            f"{certificate.certificate_id}.png"
        )

        directory = os.path.join(
            settings.MEDIA_ROOT,
            "certificates",
            "qr_codes",
        )

        os.makedirs(
            directory,
            exist_ok=True
        )

        filepath = os.path.join(
            directory,
            filename,
        )

        image.save(filepath)

        with open(filepath, "rb") as f:

            certificate.qr_code.save(
                filename,
                File(f),
                save=False,
            )

        certificate.save(
            update_fields=["qr_code"]
        )

        return certificate