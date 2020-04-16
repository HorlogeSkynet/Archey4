"""Archey's default configuration"""

CONFIGURATION = {
    'suppress_warnings': False,
    'entries': {
        'User': {
            'display_text': 'User'
        },
        'Hostname': {
            'display_text': 'Hostname'
        },
        'Model': {
            'display_text': 'Model',
            'virtual_environment_string': 'Virtual Environment'
        },
        'Distro': {
            'display_text': 'Distro'
        },
        'Kernel': {
            'display_text': 'Kernel'
        },
        'Uptime': {
            'display_text': 'Uptime'
        },
        'WindowManager': {
            'display_text': 'Window Manager'
        },
        'DesktopEnvironment': {
            'display_text': 'Desktop Environment'
        },
        'Shell': {
            'display_text': 'Shell'
        },
        'Terminal': {
            'display_text': 'Terminal'
        },
        'Packages': {
            'display_text': 'Packages'
        },
        'Temperature': {
            'display_text': 'Temperature',
            'char_before_unit': ' ',
            'use_fahrenheit': False
        },
        'CPU': {
            'display_text': 'CPU'
        },
        'GPU': {
            'display_text': 'GPU'
        },
        'RAM': {
            'display_text': 'RAM',
            'usage_warnings': {
                'warning': 33.3,
                'danger': 66.7
            }
        },
        'Disk': {
            'display_text': 'Disk',
            'usage_warnings': {
                'warning': 50,
                'danger': 75
            }
        },
        'LanIp': {
            'display_text': 'LAN IP',
            'max_count': 2,
            'ipv6_support': True
        },
        'WanIp': {
            'display_text': 'WAN IP',
            'ipv6_support': True,
            'ipv4_timeout_secs': 1.0,
            'ipv6_timeout_secs': 1.0
        }
    },
    'colors_palette': {
        'use_unicode': False
    },
    'default_strings': {
        'no_address': 'No Address',
        'not_detected': 'Not detected',
        'virtual_environment': 'Virtual Environment'
    }
}
