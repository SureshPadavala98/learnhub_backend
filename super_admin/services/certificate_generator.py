import io

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

PLATFORM_NAME = "StepUpMark"

# Keys a template's `layout` JSON may define to place a single variable's
# value at an exact pixel position on the background image, e.g.
# {"student_name": {"x": 450, "y": 220, "font_size": 32}}.
# x/y are raw pixel coordinates on the template's actual background_image
# (top-left anchor), not a ratio and not a separate design-tool canvas size.
CONTEXT_VARIABLE_KEYS = (
    "student_name",
    "course_name",
    "mentor_name",
    "issued_date",
    "certificate_id",
    "platform_name",
)

# "title"/"sub_title" are opt-in the same way (pixel dict in layout).
# Certificate background art typically already has a title baked into the
# image, so we only draw them when a template's layout explicitly supplies
# coordinates - otherwise we'd duplicate the printed title.
OPTIONAL_TEXT_FIELDS = ("title", "sub_title")

# Fallback used only when a template's layout has none of the
# CONTEXT_VARIABLE_KEYS configured yet - renders the whole description as a
# single wrapped paragraph instead of leaving the certificate blank.
# These are ratios (0-1 of image width/height) so they scale to any
# background image size.
FALLBACK_LAYOUT = {
    "description": {"x": 0.5, "y": 0.451, "font_size": 18, "color": "#16305c", "align": "center", "max_width_ratio": 0.62},
    "issued_date": {"x": 0.5, "y": 0.735, "font_size": 16, "color": "#16305c", "align": "center"},
}

# Signature/QR placement - ratio-based since these are images, not text
# variables, and scale relative to the background image's own size.
DEFAULT_OVERLAY_LAYOUT = {
    "signature": {"x": 0.251, "y": 0.775, "width_ratio": 0.155},
    "qr_code": {"x": 0.885, "y": 0.79, "width_ratio": 0.085},
}

FONT_CANDIDATES = [
    "arial.ttf",
    "DejaVuSans.ttf",
    "LiberationSans-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

BOLD_FONT_CANDIDATES = [
    "arialbd.ttf",
    "DejaVuSans-Bold.ttf",
    "LiberationSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def _load_font(size, bold=False):

    for name in (BOLD_FONT_CANDIDATES if bold else FONT_CANDIDATES):

        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue

    return ImageFont.load_default(size=size)


class CertificateGeneratorService:

    @staticmethod
    def generate(certificate):

        template = certificate.template

        if template is None:
            raise ValueError(
                "Certificate has no template assigned; cannot generate certificate file."
            )

        context = CertificateGeneratorService._build_context(certificate)
        custom_layout = template.layout or {}
        overlay_layout = CertificateGeneratorService._merged_overlay_layout(template)

        with Image.open(template.background_image.path) as source:
            image = source.convert("RGB")

        draw = ImageDraw.Draw(image)
        size = image.size

        if "title" in custom_layout:
            CertificateGeneratorService._render_pixel_text(
                draw, template.title, custom_layout["title"], bold=True
            )

        if "sub_title" in custom_layout:
            CertificateGeneratorService._render_pixel_text(
                draw, template.sub_title, custom_layout["sub_title"]
            )

        has_variable_layout = any(
            key in custom_layout for key in CONTEXT_VARIABLE_KEYS
        )

        if has_variable_layout:

            for key in CONTEXT_VARIABLE_KEYS:

                if key in custom_layout:
                    CertificateGeneratorService._render_pixel_text(
                        draw, str(context[key]), custom_layout[key]
                    )

        else:

            CertificateGeneratorService._render_text(
                draw,
                size,
                CertificateGeneratorService._render_variables(template.description, context),
                FALLBACK_LAYOUT["description"],
            )

            CertificateGeneratorService._render_text(
                draw, size, context["issued_date"], FALLBACK_LAYOUT["issued_date"]
            )

        if template.signature_image:
            CertificateGeneratorService._paste_scaled(
                image, template.signature_image.path, size, overlay_layout["signature"]
            )

        if certificate.qr_code:
            CertificateGeneratorService._paste_scaled(
                image, certificate.qr_code.path, size, overlay_layout["qr_code"]
            )

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")

        certificate.certificate_file.save(
            f"{certificate.certificate_id}.png",
            ContentFile(buffer.getvalue()),
            save=False,
        )

        certificate.save(update_fields=["certificate_file"])

        return certificate

    @staticmethod
    def _merged_overlay_layout(template):

        layout = {}
        custom_layout = template.layout or {}

        for key, defaults in DEFAULT_OVERLAY_LAYOUT.items():
            layout[key] = {**defaults, **custom_layout.get(key, {})}

        return layout

    @staticmethod
    def _build_context(certificate):

        return {
            "student_name": certificate.student_name,
            "course_name": certificate.course.title,
            "mentor_name": certificate.mentor.user.full_name,
            "issued_date": certificate.issued_date.strftime("%d %B %Y"),
            "certificate_id": certificate.certificate_id,
            "platform_name": PLATFORM_NAME,
        }

    @staticmethod
    def _render_variables(text, context):

        for key, value in context.items():
            text = text.replace("{{%s}}" % key, str(value))

        return text

    @staticmethod
    def _wrap_text(draw, text, font, max_width):

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            candidate = f"{current_line} {word}".strip()
            bbox = draw.textbbox((0, 0), candidate, font=font)

            if bbox[2] - bbox[0] <= max_width or not current_line:
                current_line = candidate
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    @staticmethod
    def _render_pixel_text(draw, text, config, bold=False):
        """Draws `text` anchored at the exact pixel (config['x'], config['y'])
        on the background image, per a template's per-variable layout entry."""

        if not text:
            return

        font_size = config.get("font_size", 24)
        font = _load_font(font_size, bold=bold)
        color = config.get("color", "#000000")
        align = config.get("align", "left")
        x = config["x"]
        y = config["y"]

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]

        if align == "center":
            draw_x = x - text_width / 2
        elif align == "right":
            draw_x = x - text_width
        else:
            draw_x = x

        draw.text((draw_x, y), text, font=font, fill=color)

    @staticmethod
    def _render_text(draw, image_size, text, config, bold=False):
        """Draws `text` wrapped/centered within a ratio-based region of the
        image - used for the fallback single-paragraph description."""

        if not text:
            return

        width, height = image_size
        font_size = config.get("font_size", 20)
        font = _load_font(font_size, bold=bold)
        color = config.get("color", "#000000")
        align = config.get("align", "center")
        x = config.get("x", 0.5) * width
        y = config.get("y", 0.5) * height

        max_width_ratio = config.get("max_width_ratio")
        lines = [text]

        if max_width_ratio:
            lines = CertificateGeneratorService._wrap_text(
                draw, text, font, max_width_ratio * width
            )

        line_height = font_size * 1.3
        current_y = y - (line_height * len(lines)) / 2

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]

            if align == "center":
                draw_x = x - line_width / 2
            elif align == "right":
                draw_x = x - line_width
            else:
                draw_x = x

            draw.text((draw_x, current_y), line, font=font, fill=color)
            current_y += line_height

    @staticmethod
    def _paste_scaled(base_image, overlay_path, base_size, config):

        width, height = base_size

        with Image.open(overlay_path) as source:
            overlay = source.convert("RGBA")

            target_width = int(config.get("width_ratio", 0.15) * width)
            scale = target_width / overlay.width
            target_height = int(overlay.height * scale)

            overlay = overlay.resize((target_width, target_height))

            paste_x = int(config.get("x", 0.5) * width - target_width / 2)
            paste_y = int(config.get("y", 0.5) * height - target_height / 2)

            base_image.paste(overlay, (paste_x, paste_y), overlay)
