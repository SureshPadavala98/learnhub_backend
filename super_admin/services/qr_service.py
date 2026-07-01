import io

import qrcode

from django.core.files.base import ContentFile


class QRCodeService:

    @staticmethod
    def generate(certificate, verify_url):

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

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")

        certificate.qr_code.save(
            f"{certificate.certificate_id}.png",
            ContentFile(buffer.getvalue()),
            save=False,
        )

        certificate.save(
            update_fields=["qr_code"]
        )

        return certificate