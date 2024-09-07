INPUT_SCHEMA = {
    'text_input': {
        'type': str,
        'required': True
    },
    'text_filtering': {
        'type': str,
        'required': False,
        'default': "none",
        'allowed': ["none", "standard", "html"]
    },
    'character_voice_gen': {
        'type': str,
        'required': False,
        'default': "female_01.wav"
    },
    'narrator_enabled': {
        'type': bool,
        'required': False,
        'default': False
    },
    'narrator_voice_gen': {
        'type': str,
        'required': False,
        'default': "male_01.wav"
    },
    'text_not_inside': {
        'type': str,
        'required': False,
        'default': "character",
        'allowed': ["character", "narrator"]
    },
    'language': {
        'type': str,
        'required': False,
        'default': "en",
        'allowed': [
            "ar", "zh-cn", "cs", "nl", "en", "fr", "de", "hi", "hu",
            "it", "ja", "ko", "pl", "pt", "ru", "es", "tr"
        ]
    },
    'output_file_name': {
        'type': str,
        'required': False,
        'default': "output"
    },
    'output_file_timestamp': {
        'type': bool,
        'required': False,
        'default': False
    },
    'autoplay': {
        'type': bool,
        'required': False,
        'default': False
    },
    'autoplay_volume': {
        'type': float,
        'required': False,
        'default': 0.8,
        'min': 0.1,
        'max': 1.0
    }
}
