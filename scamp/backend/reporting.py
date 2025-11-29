# backend/reporting.py

from __future__ import annotations

from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


ACCENT = colors.HexColor("#0B7ED0")      # primary blue
ACCENT_DARK = colors.HexColor("#09416A")
BG_LIGHT = colors.HexColor("#F5F7FA")
TEXT_DARK = colors.HexColor("#222222")
TEXT_MUTED = colors.HexColor("#555555")
BORDER = colors.HexColor("#D0D4DC")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def draw_header(c: canvas.Canvas, width: float, height: float):
    """
    Clean SOC-style header.
    """
    top_bar_height = 28

    # Top accent bar
    c.setFillColor(ACCENT)
    c.rect(0, height - top_bar_height, width, top_bar_height, fill=True, stroke=0)

    # Product / org name
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, height - top_bar_height + 8, "SCAMP Threat Intelligence")

    # Report title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, height - top_bar_height - 14, "Fraud & Deepfake Risk Assessment Report")

    # Classification tag (top right)
    c.setFillColor(colors.white)
    tag_w, tag_h = 90, 18
    x_tag = width - tag_w - 20
    y_tag = height - top_bar_height + 5
    c.roundRect(x_tag, y_tag, tag_w, tag_h, radius=4, fill=True, stroke=False)

    c.setFillColor(ACCENT_DARK)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(x_tag + tag_w / 2, y_tag + 5, "INTERNAL – AUTOMATED")


def draw_footer(c: canvas.Canvas, width: float):
    """
    Professional footer with timestamp + disclaimer.
    """
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.3)
    c.line(20 * mm, 20 * mm, width - 20 * mm, 20 * mm)

    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 8)
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    c.drawString(20 * mm, 18 * mm, "Generated automatically by SCAMP risk engine.")
    c.drawString(20 * mm, 14 * mm, "This report is advisory and may not be 100% accurate. Verify with official sources.")
    c.drawRightString(width - 20 * mm, 18 * mm, f"Generated: {ts}")
    c.drawRightString(width - 20 * mm, 14 * mm, "Page 1")


def wrap_text(c: canvas.Canvas, text: str, max_width: float, font_name="Helvetica", font_size=9):
    """
    Simple word-wrapping helper for long lines.
    """
    c.setFont(font_name, font_size)
    words = (text or "").split()
    lines = []
    current = ""

    for w in words:
        test = f"{current} {w}".strip()
        if c.stringWidth(test, font_name, font_size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def risk_bucket(score: float):
    """
    Return (color, label, description) for a given risk score.
    """
    if score >= 75:
        color = colors.HexColor("#D32F2F")   # red
        label = "HIGH RISK"
        desc = "Likely scam or deepfake activity detected."
    elif score >= 40:
        color = colors.HexColor("#F9A825")   # amber
        label = "MODERATE RISK"
        desc = "Suspicious indicators present. Review recommended."
    else:
        color = colors.HexColor("#388E3C")   # green
        label = "LOW RISK"
        desc = "No strong fraud or deepfake signals detected."
    return color, label, desc


def build_pdf_report(event: dict, out_path: Path) -> None:
    ensure_dir(out_path.parent)

    c = canvas.Canvas(str(out_path), pagesize=A4)
    width, height = A4

    # Layout constants
    left_margin = 20 * mm
    right_margin = 20 * mm
    top_margin = 40 * mm
    bottom_margin = 25 * mm
    content_width = width - left_margin - right_margin

    # === HEADER ===
    draw_header(c, width, height)

    y = height - top_margin

    def write_line(text: str, size=9, bold=False, color=TEXT_DARK, leading=12):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.setFillColor(color)
        c.drawString(left_margin, y, text)
        y -= leading

    # === EXECUTIVE SUMMARY ===
    c.setFillColor(BG_LIGHT)
    box_height = 60
    c.roundRect(left_margin, y - box_height + 10, content_width, box_height, radius=6, fill=True, stroke=0)

    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_margin + 8, y + 24, "Executive Summary")

    score = float(event.get("score", 0.0))
    label = (event.get("label", "") or "").replace("_", " ").title()
    risk_color, risk_label, risk_desc = risk_bucket(score)

    # Score badge (right side)
    badge_w, badge_h = 150, 28
    x_badge = left_margin + content_width - badge_w - 8
    y_badge = y + 10
    c.setFillColor(risk_color)
    c.roundRect(x_badge, y_badge, badge_w, badge_h, radius=6, fill=True, stroke=False)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(
        x_badge + badge_w / 2,
        y_badge + 8,
        f"{risk_label}  ({score:.1f}%)",
    )

    # Summary text
    summary_text = (
        f"SCAMP analysed the submitted media and classified it as {risk_label.lower()} "
        f"with a confidence score of {score:.1f}%. {risk_desc}"
    )
    summary_lines = wrap_text(
        c,
        summary_text,
        max_width=content_width - 16 - badge_w,
        font_name="Helvetica",
        font_size=9,
    )

    y_text = y + 16
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 9)
    for line in summary_lines:
        c.drawString(left_margin + 8, y_text, line)
        y_text -= 11

    y -= box_height + 20

    # === SECTION: CASE METADATA ===
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_margin, y, "1. Case Metadata")
    y -= 14

    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(left_margin, y, left_margin + content_width, y)
    y -= 10

    meta_rows = [
        ("Event ID", event.get("id", "N/A")),
        ("User ID", event.get("user_id", "N/A")),
        ("Platform", event.get("platform", "telegram")),
        ("Media Type", event.get("media_type", "unknown")),
        ("Model Label", label or "N/A"),
        ("Original File", event.get("file_path", "") or "N/A"),
        ("Timestamp (client)", event.get("timestamp", "N/A")),
    ]

    label_width = 35 * mm
    value_width = content_width - label_width

    c.setFont("Helvetica", 9)
    row_height = 13
    for k, v in meta_rows:
        # Key
        c.setFillColor(TEXT_MUTED)
        c.drawString(left_margin, y, f"{k}:")
        # Value (wrapped)
        c.setFillColor(TEXT_DARK)
        lines = wrap_text(c, str(v), max_width=value_width, font_name="Helvetica", font_size=9)

        first_line_y = y
        for idx, line in enumerate(lines):
            c.drawString(left_margin + label_width, first_line_y - (idx * (row_height - 3)), line)
        y -= max(row_height, row_height + (len(lines) - 1) * (row_height - 3))

        if y < bottom_margin + 60:
            # (If you later add multi-page, handle page break here)
            break

    y -= 10

    # === SECTION: RISK CLASSIFICATION & RECOMMENDATIONS ===
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_margin, y, "2. Risk Classification & Recommendations")
    y -= 14

    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(left_margin, y, left_margin + content_width, y)
    y -= 14

    # Risk explanation block
    c.setFillColor(risk_color)
    c.roundRect(left_margin, y - 36, content_width, 32, radius=6, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_margin + 8, y - 14, f"Score: {score:.2f}%  |  {risk_label}  |  {risk_desc}")
    y -= 44

    # Advisory bullets
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_margin, y, "Recommended Actions:")
    y -= 14

    bullets = [
        "Do NOT share OTPs, banking credentials, or identity documents with unverified parties.",
        "Cross-check all payment links and URLs via official bank / government websites or apps.",
        "Contact your bank and national cybercrime helpline immediately if money has already been sent.",
        "Preserve all evidence (screenshots, chat logs, transaction IDs) before deleting anything.",
    ]

    c.setFont("Helvetica", 9)
    for b in bullets:
        bullet_lines = wrap_text(c, b, max_width=content_width - 12, font_name="Helvetica", font_size=9)
        c.drawString(left_margin, y, "•")
        line_y = y
        for idx, line in enumerate(bullet_lines):
            c.drawString(left_margin + 10, line_y - idx * 11, line)
        y -= max(14, 11 * len(bullet_lines) + 2)

        if y < bottom_margin + 40:
            break

    # (Optional) section placeholder for future:
    # "3. Technical Indicators", "4. Model Version & Limitations", etc.

    # === FOOTER ===
    draw_footer(c, width)

    c.showPage()
    c.save()
