"""Human silhouettes, drawn about 100 units tall with the feet at the origin.
Each function returns SVG for a figure placed at (x, y) and scaled by s (1.0 = 100px)."""
from paint import f


def _place(x, y, s, flip, body):
    sx = -s if flip else s
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(sx)} {f(s)})">{body}</g>'


def pilgrim(x, y, s=1.0, color="#0c0a12", flip=False, rim=None):
    """A walker with a staff and a bundle on the back, heading left (flip to head right)."""
    body = (
        f'<g fill="{color}" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">'
        f'<circle cx="-5" cy="-89" r="6.6" stroke="none"/>'
        f'<path d="M-11 -92C-10 -99 0 -100 2 -92L1 -86C-3 -90 -8 -90 -11 -88Z" stroke="none"/>'
        f'<path d="M-6 -82C-1 -84 6 -83 10 -78C14 -70 15 -58 14 -46C14 -40 13 -36 12 -33L-9 -34C-10 -40 -12 -48 -17 -55'
        f'L-19 -58C-15 -62 -12 -66 -11 -70C-10 -75 -9 -79 -6 -82Z" stroke="none"/>'
        f'<ellipse cx="15" cy="-64" rx="8.5" ry="11" stroke="none" transform="rotate(12 15 -64)"/>'
        f'<path d="M4 -36L8 -18L13 -1" stroke-width="5.4" fill="none"/>'
        f'<path d="M-3 -36L-9 -19L-15 -4" stroke-width="5.4" fill="none"/>'
        f'<path d="M13 -1L18 0M-15 -4L-20 -3" stroke-width="3.4"/>'
        f'<path d="M-12 -99L-25 1" stroke-width="2.2" fill="none"/>'
        f'</g>')
    if rim:
        body += (f'<path d="M10 -78C14 -70 15 -58 14 -46" stroke="{rim}" stroke-width="1.3" fill="none" opacity=".8"/>'
                 f'<path d="M1 -94C1 -88 -1 -84 -4 -82" stroke="{rim}" stroke-width="1.1" fill="none" opacity=".7"/>')
    return _place(x, y, s, flip, body)


def seated(x, y, s=1.0, color="#0c0a12", rim=None, hands="lap"):
    """A meditator in lotus posture seen from the front; (x, y) is the base of the crossed legs."""
    arms = ('<path d="M-17 -50C-24 -38 -22 -24 -12 -16L-4 -16C-12 -24 -14 -36 -11 -46Z"/>'
            '<path d="M17 -50C24 -38 22 -24 12 -16L4 -16C12 -24 14 -36 11 -46Z"/>') if hands == "lap" else (
            '<path d="M-17 -50C-26 -40 -30 -26 -34 -18L-28 -15C-24 -24 -18 -34 -11 -44Z"/>'
            '<path d="M17 -50C26 -40 30 -26 34 -18L28 -15C24 -24 18 -34 11 -44Z"/>')
    body = (
        f'<g fill="{color}">'
        f'<circle cx="0" cy="-74" r="9"/>'
        f'<path d="M-6 -78C-8 -88 0 -94 7 -88C9 -86 9 -82 8 -79C4 -86 -2 -86 -6 -78Z"/>'
        f'<ellipse cx="0" cy="-85" rx="5.5" ry="4.2"/>'
        f'<path d="M-5 -66H5L6 -62C12 -60 17 -56 18 -50C19 -40 16 -28 14 -18H-14C-16 -28 -19 -40 -18 -50C-17 -56 -12 -60 -6 -62Z"/>'
        f'{arms}'
        f'<path d="M-40 -6C-38 -16 -24 -20 -6 -18H6C24 -20 38 -16 40 -6C40 -1 34 1 24 1H-24C-34 1 -40 -1 -40 -6Z"/>'
        f'</g>')
    if rim:
        body += f'<path d="M7 -82C10 -78 10 -70 6 -66M18 -50C19 -40 16 -28 14 -18" stroke="{rim}" stroke-width="1.2" fill="none" opacity=".8"/>'
    return _place(x, y, s, False, body)


def priest_aarti(x, y, s=1.0, color="#0c0a12", flip=False):
    """A priest in a dhoti raising a tiered aarti lamp; returns (svg, lamp_x, lamp_y) in scene units."""
    body = (
        f'<g fill="{color}" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">'
        f'<circle cx="0" cy="-88" r="6.4" stroke="none"/>'
        f'<path d="M-9 -80C-4 -82 4 -82 9 -80L11 -60C11 -54 10 -48 9 -44L-9 -44C-10 -48 -11 -54 -11 -60Z" stroke="none"/>'
        f'<path d="M-10 -46L-12 -24L-14 0H-6L-2 -26L2 -26L6 0H14L12 -24L10 -46Z" stroke="none"/>'
        f'<path d="M9 -78L18 -88L22 -106" stroke-width="5" fill="none"/>'
        f'<path d="M-9 -78L-18 -66L-10 -56" stroke-width="5" fill="none"/>'
        f'<path d="M22 -106V-112" stroke-width="2.4"/>'
        f'<path d="M10 -112H34L30 -116H14Z M13 -120H31L28 -124H16Z M16 -128H28L26 -132H18Z" stroke-width="1"/>'
        f'</g>')
    lx = x + (-22 if flip else 22) * s
    return _place(x, y, s, flip, body), lx, y - 124 * s


def sitter(x, y, s=1.0, color="#0c0a12", flip=False):
    """Someone sitting on a step, knees drawn up, seen side-on."""
    body = (
        f'<g fill="{color}">'
        f'<circle cx="2" cy="-58" r="6.2"/>'
        f'<path d="M-6 -50C-2 -53 6 -52 8 -48L10 -30C10 -24 8 -20 4 -18H-10C-12 -24 -10 -40 -6 -50Z"/>'
        f'<path d="M4 -18L22 -26L26 -22L24 0H18L18 -16L2 -10Z"/>'
        f'<path d="M6 -46L18 -34L22 -26L18 -24L10 -32Z"/>'
        f'</g>')
    return _place(x, y, s, flip, body)


def rower(x, y, s=1.0, color="#0c0a12", flip=False):
    """A boatman standing at the stern with a long oar."""
    body = (
        f'<g fill="{color}" stroke="{color}" stroke-linecap="round">'
        f'<circle cx="0" cy="-58" r="5"/>'
        f'<path d="M-6 -52H6L7 -30L4 0H-4L-7 -30Z" stroke="none"/>'
        f'<path d="M5 -48L16 -40M-5 -48L10 -36" stroke-width="3.4"/>'
        f'<path d="M22 -62L-10 30" stroke-width="2"/>'
        f'</g>')
    return _place(x, y, s, flip, body)
