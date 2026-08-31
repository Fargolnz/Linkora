"""HTML generation for validated Linkora documents.

Every block type has a ``render_<block>`` function. The dispatch table at the
bottom of this module maps block names to their renderer, so adding a new
block requires registering a single new renderer.
"""

from __future__ import annotations

import html

from compiler.ast import Block, Document
from compiler.codegen.css import build_css


#: Per-platform metadata for the SocialMedia block: canonical display name,
#: a full-color brand SVG icon (inline path data), and a soft shade of the
#: brand color used as the default item background.
PLATFORM_META: dict[str, dict[str, str]] = {
    "instagram": {
        "name": "Instagram",
        "bg": "#F3E9F2",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<defs><linearGradient id="ig" x1="0" y1="1" x2="1" y2="0">'
            '<stop offset="0" stop-color="#F09433"/><stop offset="0.25" '
            'stop-color="#E6683C"/><stop offset="0.5" stop-color="#DC2743"/>'
            '<stop offset="0.75" stop-color="#CC2366"/><stop offset="1" '
            'stop-color="#BC1888"/></linearGradient></defs>'
            '<path fill="url(#ig)" d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.'
            '5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.'
            '3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.'
            '6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 '
            '2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 '
            '1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.'
            '069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.1'
            '47-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 '
            '1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.'
            '2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.06'
            '07-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.'
            '1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 '
            '16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.'
            '0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-'
            '.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.16'
            '44-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848'
            '-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.'
            '216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.'
            '423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.07'
            '9 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.'
            '408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.'
            '1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.'
            '0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294'
            '-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224'
            '.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.'
            '2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 '
            '4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 '
            '6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.'
            '4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738'
            'M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/>'
            "</svg>"
        ),
    },
    "telegram": {
        "name": "Telegram",
        "bg": "#E3F2FD",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#26A5E4" d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 '
            '12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 '
            '7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.'
            '306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 '
            '1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.'
            '185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.'
            '014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.'
            '345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-'
            '1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.'
            '529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>'
            "</svg>"
        ),
    },
    "youtube": {
        "name": "YouTube",
        "bg": "#FDE9E9",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#FF0000" d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136'
            'C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 '
            '.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 '
            '2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 '
            '0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 '
            '15.568V8.432L15.818 12l-6.273 3.568z"/>'
            "</svg>"
        ),
    },
    "tiktok": {
        "name": "TikTok",
        "bg": "#E9F1F7",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#FE2C55" d="M14.293 1.155a6.21 6.21 0 0 1 2.579 3.133 '
            '5.36 5.36 0 0 0 4.728 2.213v3.25c-1.605.02-3.143-.33-4.368-1.049v5.785'
            'a6.673 6.673 0 1 1-6.673-6.672c.341 0 .678.025 1.008.074v3.368a3.26 '
            '3.26 0 0 0-1.008-.157 3.29 3.29 0 1 0 3.29 3.29V1.155z"/>'
            '<path fill="#000000" d="M14.293.012c.084 1.77 1.025 3.374 2.416 '
            '4.332a5.37 5.37 0 0 0 4.891.787v3.633c-1.476.133-2.912-.25-4.195-1.019'
            'v6.98a6.673 6.673 0 1 1-6.673-6.673c.314 0 .623.022.925.064v3.686c-.3'
            '-.05-.6-.077-.94-.077a3.067 3.067 0 1 0 3.066 3.067V.012h1.51z"/>'
            "</svg>"
        ),
    },
    "x": {
        "name": "X",
        "bg": "#ECECEC",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#000000" d="M14.234 10.162 22.977 0h-2.072l-7.591 '
            '8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24'
            'h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 '
            '1.329 7.754 11.09h-3.182z"/>'
            "</svg>"
        ),
    },
    "linkedin": {
        "name": "LinkedIn",
        "bg": "#E7EEF7",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#0A66C2" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.'
            '037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v'
            '1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 '
            '5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.'
            '92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 '
            '2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771'
            'C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 '
            '24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>'
            "</svg>"
        ),
    },
    "github": {
        "name": "GitHub",
        "bg": "#E9ECEF",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#181717" d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 '
            '3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.'
            '04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7'
            'c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07'
            ' 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.'
            '466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.'
            '105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 '
            '2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.'
            '12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.'
            '36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57'
            'C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>'
            "</svg>"
        ),
    },
    "spotify": {
        "name": "Spotify",
        "bg": "#E4F4E8",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#1DB954" d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 '
            '12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.'
            '36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.'
            '54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3'
            'c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.'
            '02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84'
            'c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.'
            '179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 '
            '15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>'
            "</svg>"
        ),
    },
    "twitch": {
        "name": "Twitch",
        "bg": "#EAE6F8",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#9146FF" d="M11.571 4.714h1.715v5.143H11.57zm4.715 0H18'
            'v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.'
            '286 12V0zm14.571 11.143l-3.428 3.428h-3.429l-3 3v-3H6.857V1.714h13.'
            '714Z"/>'
            "</svg>"
        ),
    },
    "pinterest": {
        "name": "Pinterest",
        "bg": "#F9E7E4",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#BD081C" d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 '
            '5.079 3.158 9.417 7.618 11.162-.105-.949-.199-2.403.041-3.439.219-.'
            '937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 '
            '2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.'
            '992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 '
            '0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 '
            '1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.'
            '334 1.363-.053.225-.172.271-.401.165-1.495-.69-2.433-2.878-2.433-4.'
            '646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 '
            '4.135-2.607 7.462-6.233 7.462-1.214 0-2.354-.629-2.758-1.379l-.749 '
            '2.848c-.269 1.045-1.004 2.352-1.498 3.146 1.123.345 2.306.535 3.55.'
            '535 6.607 0 11.985-5.365 11.985-11.987C23.97 5.39 18.592.026 11.985.'
            '026L12.017 0z"/>'
            "</svg>"
        ),
    },
    "facebook": {
        "name": "Facebook",
        "bg": "#E7EFFB",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#1877F2" d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58'
            'c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 '
            '0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 '
            '0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.'
            '258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246'
            'v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 '
            '5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/>'
            "</svg>"
        ),
    },
    "patreon": {
        "name": "Patreon",
        "bg": "#FDE9E6",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#FF424D" d="M22.957 7.21c-.004-3.064-2.391-5.576-5.191-'
            '6.482-3.478-1.125-8.064-.962-11.384.604C2.357 3.231 1.093 7.391 1.046 '
            '11.54c-.039 3.411.302 12.396 5.369 12.46 3.765.047 4.326-4.804 6.068-'
            '7.141 1.24-1.662 2.836-2.132 4.801-2.618 3.376-.836 5.678-3.501 5.673'
            '-7.031Z"/>'
            "</svg>"
        ),
    },
}

NETWORK_META: dict[str, dict[str, str]] = {
    "telegram": {
        "name": "Telegram",
        "bg": "#E3F2FD",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#0088CC" d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 '
            '12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 '
            '7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.'
            '306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 '
            '1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.'
            '185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.'
            '014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.'
            '345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-'
            '1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.'
            '529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>'
            "</svg>"
        ),
    },
    "whatsapp": {
        "name": "WhatsApp",
        "bg": "#E3FBE6",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#25D366" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967'
            '-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347'
            '.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761'
            '-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52'
            '.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669'
            '-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57'
            '-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462'
            ' 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262'
            '.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006'
            '-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m'
            '-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982'
            '.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884'
            ' 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893'
            ' 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815'
            ' 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588'
            ' 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554'
            ' 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>'
            "</svg>"
        ),
    },
    "discord": {
        "name": "Discord",
        "bg": "#E8EAFB",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#5865F2" d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851'
            '-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495'
            '-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495'
            'a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699'
            ' 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00'
            '.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00'
            '.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416'
            '-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076'
            '-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105'
            'c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202'
            '.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01'
            '-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225'
            ' 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023'
            '-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485'
            '-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569'
            '-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757'
            ' 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0'
            'c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569'
            '-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189'
            '-2.1568 2.4189Z"/>'
            "</svg>"
        ),
    },
    "skype": {
        "name": "Skype",
        "bg": "#E3F9FF",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#00AFF0" d="M12.069 18.874c-4.023 0-5.82-1.979-5.82'
            '-3.464c0-.765.561-1.296 1.333-1.296c1.723 0 1.273 2.477 4.487 2.477'
            'c1.641 0 2.55-.895 2.55-1.811c0-.551-.269-1.16-1.354-1.429l-3.576'
            '-.895c-2.88-.724-3.403-2.286-3.403-3.751c0-3.047 2.861-4.191 5.549'
            '-4.191c2.471 0 5.393 1.373 5.393 3.199c0 .784-.688 1.24-1.453 1.24'
            'c-1.469 0-1.198-2.037-4.164-2.037c-1.469 0-2.292.664-2.292 1.617s'
            '1.153 1.258 2.157 1.487l2.637.587c2.891.649 3.624 2.346 3.624 3.944'
            'c0 2.476-1.902 4.324-5.722 4.324m11.084-4.882l-.029.135l-.044-.24c'
            '.015.045.044.074.059.12c.12-.675.181-1.363.181-2.052a11.32 11.32 0 0 0'
            '-3.325-8.016a11.5 11.5 0 0 0-3.595-2.426c-1.318-.631-2.801-.93-4.328'
            '-.93c-.72 0-1.444.07-2.143.204l.119.06l-.239-.033l.119-.025A6.7 6.7 0'
            ' 0 0 6.731 0c-1.789 0-3.47.698-4.736 1.967A6.68 6.68 0 0 0 .032 6.716'
            'c0 1.143.292 2.265.844 3.258l.02-.124l.041.239l-.06-.115a11.4 11.4 0'
            ' 0 0 .712 6.371a10.9 10.9 0 0 0 2.427 3.609a11.3 11.3 0 0 0 3.595'
            ' 2.442c1.394.6 2.877.898 4.404.898c.659 0 1.334-.06 1.977-.179l-.119'
            '-.062l.24.046l-.135.03a6.64 6.64 0 0 0 3.294.871a6.64 6.64 0 0 0'
            ' 4.733-1.963a6.68 6.68 0 0 0 1.962-4.749a6.8 6.8 0 0 0-.853-3.266"/>'
            "</svg>"
        ),
    },
    "line": {
        "name": "LINE",
        "bg": "#E3FBE3",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#00B900" d="M19.365 9.863c.349 0 .63.285.63.631 0'
            ' .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0'
            ' .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108'
            'c0-.345.282-.63.63-.63h2.386c.346 0 .627.285.627.63 0 .349-.281'
            '.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432'
            '.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443'
            '-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629'
            'V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0'
            ' .375.104.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0'
            ' .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345'
            ' 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63.346 0 .628'
            '.285.628.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629'
            'V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756'
            'c.348 0 .629.283.629.63 0 .344-.282.629-.629.629M24 10.314C24'
            ' 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842'
            ' 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08'
            'l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078'
            ' 9.436-6.975C23.176 14.393 24 12.458 24 10.314"/>'
            "</svg>"
        ),
    },
    "viber": {
        "name": "Viber",
        "bg": "#ECEAFD",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#7360F2" d="M11.4 0C9.473.028 5.333.344 3.02 2.467'
            ' 1.302 4.187.696 6.7.633 9.817.57 12.933.488 18.776 6.12 20.36h.003'
            'l-.004 2.416s-.037.977.61 1.177c.777.242 1.234-.5 1.98-1.302.407-.44'
            '.972-1.084 1.397-1.58 3.85.326 6.812-.416 7.15-.525.776-.252 5.176'
            '-.816 5.892-6.657.74-6.02-.36-9.83-2.34-11.546-.596-.55-3.006-2.3'
            '-8.375-2.323 0 0-.395-.025-1.037-.017zm.058 1.693c.545-.004.88'
            '.017.88.017 4.542.02 6.717 1.388 7.222 1.846 1.675 1.435 2.53 4.868'
            ' 1.906 9.897v.002c-.604 4.878-4.174 5.184-4.832 5.395-.28.09-2.882'
            '.737-6.153.524 0 0-2.436 2.94-3.197 3.704-.12.12-.26.167-.352.144'
            '-.13-.033-.166-.188-.165-.414l.02-4.018c-4.762-1.32-4.485-6.292'
            '-4.43-8.895.054-2.604.543-4.738 1.996-6.173 1.96-1.773 5.474-2.018'
            ' 7.11-2.03zm.38 2.602c-.167 0-.303.135-.304.302 0 .167.133.303.3'
            '.305 1.624.01 2.946.537 4.028 1.592 1.073 1.046 1.62 2.468 1.633'
            ' 4.334.002.167.14.3.307.3.166-.002.3-.138.3-.304-.014-1.984-.618'
            '-3.596-1.816-4.764-1.19-1.16-2.692-1.753-4.447-1.765zm-3.96.695'
            'c-.19-.032-.4.005-.616.117l-.01.002c-.43.247-.816.562-1.146.932'
            '-.002.004-.006.004-.008.008-.267.323-.42.638-.46.948-.008.046-.01'
            '.093-.007.14 0 .136.022.27.065.4l.013.01c.135.48.473 1.276 1.205'
            ' 2.604.42.768.903 1.5 1.446 2.186.27.344.56.673.87.984l.132.132'
            'c.31.308.64.6.984.87.686.543 1.418 1.027 2.186 1.447 1.328.733'
            ' 2.126 1.07 2.604 1.206l.01.014c.13.042.265.064.402.063.046.002'
            '.092 0 .138-.008.31-.036.627-.19.948-.46.004 0 .003-.002.008-.005'
            '.37-.33.683-.72.93-1.148l.003-.01c.225-.432.15-.842-.18-1.12-.004'
            ' 0-.698-.58-1.037-.83-.36-.255-.73-.492-1.113-.71-.51-.285-1.032'
            '-.106-1.248.174l-.447.564c-.23.283-.657.246-.657.246-3.12-.796'
            '-3.955-3.955-3.955-3.955s-.037-.426.248-.656l.563-.448c.277-.215'
            '.456-.737.17-1.248-.217-.383-.454-.756-.71-1.115-.25-.34-.826'
            '-1.033-.83-1.035-.137-.165-.31-.265-.502-.297zm4.49.88c-.158.002'
            '-.29.124-.3.282-.01.167.115.312.282.324 1.16.085 2.017.466 2.645'
            ' 1.15.63.688.93 1.524.906 2.57-.002.168.13.306.3.31.166.003.305'
            '-.13.31-.297.025-1.175-.334-2.193-1.067-2.994-.74-.81-1.777-1.253'
            '-3.05-1.346h-.024zm.463 1.63c-.16.002-.29.127-.3.287-.008.167.12'
            '.31.288.32.523.028.875.175 1.113.422.24.245.388.62.416 1.164.01'
            '.167.15.295.318.287.167-.008.295-.15.287-.317-.03-.644-.215-1.178'
            '-.58-1.557-.367-.378-.893-.574-1.52-.607h-.018z"/>'
            "</svg>"
        ),
    },
    "kik": {
        "name": "Kik",
        "bg": "#F3FBE3",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#82B208" d="M11.482 16.752c-.01.688-.56 1.242-1.238'
            ' 1.242-.689 0-1.23-.541-1.244-1.23h-.016v-6.243H9v-.029c0-.693.556'
            '-1.256 1.237-1.256s1.236.563 1.236 1.258v.045h.016v6.225h-.016l.009'
            '-.012zm11.137-4.889c.75 0 1.381.618 1.381 1.377 0 .76-.631 1.375'
            '-1.381 1.375-.766 0-1.395-.615-1.395-1.379 0-.766.615-1.381 1.379'
            '-1.381l.016.008zm-2.084 4.186c.121.195.193.432.193.686 0 .703-.553'
            ' 1.26-1.244 1.26-.463 0-.869-.256-1.08-.631l-2.053-2.746-.631.586'
            'v1.635h-.014c-.039.652-.57 1.168-1.225 1.168-.674 0-1.221-.553'
            '-1.221-1.238v-.025h-.016v-9.45h.027v-.047c0-.69.551-1.253 1.23'
            '-1.253.674 0 1.225.562 1.225 1.253v.07h.016l.01 4.597 2.311-2.261'
            'c.229-.255.559-.405.928-.405.689 0 1.248.57 1.248 1.26 0 .346-.133'
            '.646-.344.871l.012.015-1.621 1.605 2.281 3.061-.016.016-.016-.027'
            'zm-13.246 0c.12.195.195.432.195.686 0 .703-.555 1.26-1.244 1.26'
            '-.466 0-.871-.256-1.081-.631l-2.054-2.746-.63.586v1.631H2.46c-.036'
            '.654-.57 1.17-1.221 1.17-.676 0-1.225-.555-1.225-1.238v-.027H0V7.29'
            'h.031c-.004-.015-.004-.029-.004-.044 0-.69.551-1.252 1.23-1.252.675'
            ' 0 1.225.559 1.225 1.25v.07h.016l.01 4.6 2.311-2.261c.23-.255.562'
            '-.405.931-.405.687 0 1.245.57 1.245 1.26 0 .33-.131.646-.346.871'
            'l.016.015-1.627 1.605 2.271 3.061-.016.016-.004-.027z"/>'
            "</svg>"
        ),
    },
    "facebookMessenger": {
        "name": "Messenger",
        "bg": "#E3F0FC",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#0668E1" d="M12 0C5.24 0 0 4.952 0 11.64c0 3.499 1.434'
            ' 6.521 3.769 8.61a.96.96 0 0 1 .323.683l.065 2.135a.96.96 0 0 0'
            ' 1.347.85l2.381-1.053a.96.96 0 0 1 .641-.046A13 13 0 0 0 12 23.28'
            'c6.76 0 12-4.952 12-11.64S18.76 0 12 0m6.806 7.44c.522-.03.971.567'
            '.63 1.094l-4.178 6.457a.707.707 0 0 1-.977.208l-3.87-2.504a.44.44'
            ' 0 0 0-.49.007l-4.363 3.01c-.637.438-1.415-.317-.995-.966l4.179-6.457'
            'a.706.706 0 0 1 .977-.21l3.87 2.505c.15.097.344.094.491-.007l4.362'
            '-3.008a.7.7 0 0 1 .364-.13"/>'
            "</svg>"
        ),
    },
}


def render_html(document: Document) -> str:
    """Render a validated document into a complete HTML page."""
    body = "\n".join(_render_block(block) for block in document.blocks)

    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\">\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
        "  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n"
        "  <link href=\"https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700&display=swap\" rel=\"stylesheet\">\n"
        "  <title>Linkora</title>\n"
        "  <style>\n"
        f"{build_css()}"
        "  </style>\n"
        "</head>\n"
        "<body>\n"
        f"  <main class=\"lk-page\">\n{body}\n  </main>\n"
        "</body>\n"
        "</html>\n"
    )


def _render_block(block: Block) -> str:
    renderer = _RENDERERS.get(block.name)
    if renderer is None:
        return f"<!-- unsupported block: {html.escape(block.name)} -->"
    return renderer(block)


_PROFILE_CHILD_ORDER = ["Cover", "Logo", "Name", "Bio"]


def render_profile(block: Block) -> str:
    """Render a Profile container, sorting children into display order."""
    sorted_children = sorted(
        block.children,
        key=lambda c: _PROFILE_CHILD_ORDER.index(c.name)
        if c.name in _PROFILE_CHILD_ORDER
        else len(_PROFILE_CHILD_ORDER),
    )
    inner = "\n".join(_render_block(child) for child in sorted_children)
    return f'  <section class="lk-profile">\n{inner}\n  </section>'


def render_name(block: Block) -> str:
    """Render a Name block with title and subtitle."""
    resolved = block.resolved
    title = str(resolved["title"])
    subtitle = str(resolved["subtitle"])
    align = str(resolved["align"])
    title_color = str(resolved["titleColor"])
    sub_color = str(resolved["subColor"])

    parts = []
    if title:
        parts.append(
            f'    <h1 class="lk-name-title" '
            f'style="color: {title_color};">{html.escape(title)}</h1>'
        )
    if subtitle:
        parts.append(
            f'    <p class="lk-name-subtitle" '
            f'style="color: {sub_color};">{html.escape(subtitle)}</p>'
        )

    inner = "\n".join(parts)
    return (
        f'  <div class="lk-name lk-align-{align}">\n'
        f"{inner}\n"
        f"  </div>"
    )


def render_logo(block: Block) -> str:
    """Render a Logo block as a profile image."""
    resolved = block.resolved
    image = str(resolved["image"])
    shape = str(resolved["shape"])
    border_color = str(resolved["borderColor"])

    style = f"border-color: {border_color};"
    return (
        f'    <img class="lk-logo lk-logo-{shape}" '
        f'style="{style}" '
        f'src="{html.escape(image, quote=True)}" alt="Logo">'
    )


def render_bio(block: Block) -> str:
    """Render a Bio block as a styled paragraph."""
    resolved = block.resolved
    text = str(resolved["text"])
    align = str(resolved["align"])
    text_color = str(resolved["textColor"])
    bg_color = str(resolved["backgroundColor"])
    border_color = str(resolved["borderColor"])
    shape = str(resolved["shape"])

    classes = " ".join(["lk-bio", f"lk-shape-{shape}"])
    style = (
        f"color: {text_color}; "
        f"background-color: {bg_color}; "
        f"border-color: {border_color}; "
        f"text-align: {align};"
    )
    return (
        f'    <p class="{classes}" style="{style}">'
        f"{html.escape(text)}</p>"
    )


def render_cover(block: Block) -> str:
    """Render a Cover block as a full-width banner image."""
    resolved = block.resolved
    image = str(resolved["image"])
    shape = str(resolved["shape"])

    classes = " ".join(["lk-cover", f"lk-cover-{shape}"])
    return (
        f'  <div class="{classes}">\n'
        f'    <img class="lk-cover-img" '
        f'src="{html.escape(image, quote=True)}" alt="Cover">\n'
        f"  </div>"
    )


def render_link(block: Block) -> str:
    """Render a Link block as a clickable, styled button."""
    resolved = block.resolved
    title = str(resolved["title"])
    url = str(resolved["url"])
    shape = str(resolved["shape"])
    align = str(resolved["align"])
    title_color = str(resolved["titleColor"])
    background_color = str(resolved["backgroundColor"])
    border_color = str(resolved["borderColor"])

    classes = " ".join(["lk-link", f"lk-shape-{shape}", f"lk-align-{align}"])
    style = (
        f"color: {title_color}; "
        f"background-color: {background_color}; "
        f"border-color: {border_color};"
    )

    return (
        f'    <a class="{classes}" style="{style}" '
        f'href="{html.escape(url, quote=True)}">'
        f"{html.escape(title)}</a>"
    )


def render_title(block: Block) -> str:
    """Render a Title block as a styled heading."""
    resolved = block.resolved
    title = str(resolved["title"])
    align = str(resolved["align"])
    title_color = str(resolved["titleColor"])

    style = f"color: {title_color}; text-align: {align};"

    return (
        f'  <h2 class="lk-title" style="{style}">'
        f"{html.escape(title)}</h2>"
    )


def render_text(block: Block) -> str:
    """Render a Text block as a styled paragraph."""
    resolved = block.resolved
    text = str(resolved["text"])
    align = str(resolved["align"])
    text_color = str(resolved["textColor"])
    bg_color = str(resolved["backgroundColor"])
    border_color = str(resolved["borderColor"])
    shape = str(resolved["shape"])

    classes = " ".join(["lk-text", f"lk-shape-{shape}"])
    style = (
        f"color: {text_color}; "
        f"background-color: {bg_color}; "
        f"border-color: {border_color}; "
        f"text-align: {align};"
    )
    return (
        f'  <p class="{classes}" style="{style}">'
        f"{html.escape(text)}</p>"
    )


def render_socialmedia_item(block: Block) -> str:
    """Render a single SocialMedia item as a clickable styled button."""
    resolved = block.resolved
    parent = _parent_resolved(block)
    platform = str(resolved["platform"])
    meta = PLATFORM_META[platform]

    def inherit(key: str, parent_key: str, fallback: str = "") -> str:
        value = str(resolved[key])
        if value:
            return value
        pvalue = str(parent.get(parent_key, ""))
        if pvalue:
            return pvalue
        return fallback

    title = str(resolved["title"]) or meta["name"]
    url = str(resolved["url"])
    title_color = inherit("titleColor", "titleColor", "#1A1A1A")
    background_color = inherit("backgroundColor", "backgroundColor", meta["bg"])
    border_color = inherit("borderColor", "borderColor", "transparent")
    icon_color = str(resolved["iconColor"]) or str(parent.get("iconColor", "")) or ""

    show_title = bool(parent.get("showTitle", True))
    show_icon = bool(parent.get("showIcon", True))
    icon_position = str(parent.get("iconPosition", "right"))
    shape = str(parent.get("shape", "rounded"))

    classes = " ".join(
        ["lk-socialitem", f"lk-shape-{shape}", f"lk-icon-{icon_position}"]
    )
    style = (
        f"color: {title_color}; "
        f"background-color: {background_color}; "
        f"border-color: {border_color};"
    )

    parts = []
    if show_icon:
        parts.append(_icon_svg(meta, icon_color))
    if show_title:
        parts.append(f'<span class="lk-socialitem-title">{html.escape(title)}</span>')

    inner = "".join(parts)
    return (
        f'    <a class="{classes}" style="{style}" '
        f'href="{html.escape(url, quote=True)}">{inner}</a>'
    )


def render_socialmedia(block: Block) -> str:
    """Render a SocialMedia container as a responsive grid of items."""
    resolved = block.resolved
    columns = int(resolved["columns"])
    items_order = str(resolved["itemsOrder"])

    items = "\n".join(_render_block(child) for child in block.children)
    return (
        f'  <section class="lk-social" '
        f'data-columns="{columns}" data-order="{items_order}">\n'
        f"{items}\n"
        f"  </section>"
    )


def render_socialnetwork_item(block: Block) -> str:
    """Render a single SocialNetwork item as a clickable styled button."""
    resolved = block.resolved
    parent = _parent_resolved(block)
    platform = str(resolved["platform"])
    meta = NETWORK_META[platform]

    def inherit(key: str, parent_key: str, fallback: str = "") -> str:
        value = str(resolved[key])
        if value:
            return value
        pvalue = str(parent.get(parent_key, ""))
        if pvalue:
            return pvalue
        return fallback

    title = str(resolved["title"]) or meta["name"]
    url = str(resolved["url"])
    title_color = inherit("titleColor", "titleColor", "#3B3B3B")
    background_color = inherit("backgroundColor", "backgroundColor", meta["bg"])
    border_color = inherit("borderColor", "borderColor", "transparent")
    icon_color = str(resolved["iconColor"]) or str(parent.get("iconColor", "")) or ""

    show_title = bool(parent.get("showTitle", True))
    show_icon = bool(parent.get("showIcon", True))
    icon_position = str(parent.get("iconPosition", "right"))
    shape = str(parent.get("shape", "rounded"))

    classes = " ".join(
        ["lk-socialitem", f"lk-shape-{shape}", f"lk-icon-{icon_position}"]
    )
    style = (
        f"color: {title_color}; "
        f"background-color: {background_color}; "
        f"border-color: {border_color};"
    )

    parts = []
    if show_icon:
        parts.append(_icon_svg(meta, icon_color))
    if show_title:
        parts.append(f'<span class="lk-socialitem-title">{html.escape(title)}</span>')

    inner = "".join(parts)
    return (
        f'    <a class="{classes}" style="{style}" '
        f'href="{html.escape(url, quote=True)}">{inner}</a>'
    )


def render_socialnetwork(block: Block) -> str:
    """Render a SocialNetwork container as a responsive grid of items."""
    resolved = block.resolved
    columns = int(resolved["columns"])
    items_order = str(resolved["itemsOrder"])

    items = "\n".join(_render_block(child) for child in block.children)
    return (
        f'  <section class="lk-social" '
        f'data-columns="{columns}" data-order="{items_order}">\n'
        f"{items}\n"
        f"  </section>"
    )


def _parent_resolved(block: Block) -> dict[str, object]:
    """Return the resolved properties of the nearest ancestor block."""
    return block.parent.resolved if block.parent is not None else {}


def _icon_svg(meta: dict[str, str], icon_color: str) -> str:
    """Wrap a platform's inline SVG, optionally forcing a single icon color.

    When ``icon_color`` is set, every hex fill, stroke and gradient stop is
    recolored, so both flat and full-color (gradient / multi-layer) icons are
    tinted to the requested color.
    """
    svg = meta["icon"]
    if icon_color:
        import re

        tint = html.escape(icon_color, quote=True)
        svg = re.sub(r'fill="#[0-9a-fA-F]{3,8}"', f'fill="{tint}"', svg)
        svg = re.sub(r'stroke="#[0-9a-fA-F]{3,8}"', f'stroke="{tint}"', svg)
        svg = re.sub(
            r'stop-color="#[0-9a-fA-F]{3,8}"', f'stop-color="{tint}"', svg
        )
    return f'<span class="lk-socialitem-icon" aria-hidden="true">{svg}</span>'


#: Dispatch table mapping block names to their HTML renderers.
_RENDERERS = {
    "Profile": render_profile,
    "Name": render_name,
    "Logo": render_logo,
    "Bio": render_bio,
    "Cover": render_cover,
    "Link": render_link,
    "Title": render_title,
    "Text": render_text,
    "SocialMedia": render_socialmedia,
    "SocialMediaItem": render_socialmedia_item,
    "SocialNetwork": render_socialnetwork,
    "SocialNetworkItem": render_socialnetwork_item,
}
