import asyncio
import re
import uuid
import time
import hashlib
from pathlib import Path

# Assuming these functions are defined elsewhere
from tts_server import generate_audio, combine, process_text, play_audio

async def generate(
    text_input: str,
    text_filtering: str,
    character_voice_gen: str,
    narrator_enabled: bool,
    narrator_voice_gen: str,
    text_not_inside: str,
    language: str,
    output_file_name: str,
    output_file_timestamp: bool,
    autoplay: bool,
    autoplay_volume: float,
    streaming: bool = False,
    temperature: float = 1.0,
    repetition_penalty: float = 1.0
):
    try:
        # Path where you will store the audio file
        this_dir = Path(__file__).parent
        output_dir = this_dir / "outputs"
        output_dir.mkdir(exist_ok=True)  # Create the directory if it doesn't exist
        
        if narrator_enabled:
            processed_parts = process_text(text_input)
            audio_files_all_paragraphs = []
            
            for part_type, part in processed_parts:
                if len(part.strip()) <= 3:
                    continue  # Skip parts that are too short

                # Determine voice to use
                if part_type == 'narrator':
                    voice_to_use = narrator_voice_gen
                elif part_type == 'character':
                    voice_to_use = character_voice_gen
                else:
                    voice_to_use = character_voice_gen if text_not_inside == "character" else narrator_voice_gen

                # Clean the input text
                cleaned_part = re.sub(r'([!?.\u3002\uFF1F\uFF01\uFF0C])\1+', r'\1', part)
                cleaned_part = re.sub(r"\u2026{1,2}", ". ", cleaned_part)
                cleaned_part = re.sub(r'[^a-zA-Z0-9\s.,;:!?\-\'"$]', '', cleaned_part)

                # Generate the audio file
                output_file = output_dir / f"{output_file_name}_{uuid.uuid4()}_{int(time.time())}.wav"
                await generate_audio(cleaned_part, voice_to_use, language, temperature, repetition_penalty, output_file.as_posix(), streaming)
                audio_files_all_paragraphs.append(output_file.as_posix())

            # Combine all generated audio files
            output_file_path, output_file_url, output_cache_url = combine(output_file_timestamp, output_file_name, audio_files_all_paragraphs)

        else:
            if output_file_timestamp:
                timestamp = int(time.time())
                short_uuid = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:5]
                output_file_path = output_dir / f"{output_file_name}_{timestamp}{short_uuid}.wav"
            else:
                output_file_path = output_dir / f"{output_file_name}.wav"

            # Apply text filtering and generate audio
            if text_filtering == "html":
                cleaned_string = re.sub(r'([!?.\u3002\uFF1F\uFF01\uFF0C])\1+', r'\1', text_input)
            else:
                cleaned_string = text_input

            await generate_audio(cleaned_string, character_voice_gen, language, temperature, repetition_penalty, output_file_path.as_posix(), streaming)

        # Autoplay functionality if enabled
        if autoplay:
            play_audio(output_file_path, autoplay_volume)

        return {"status": "generate-success", "output_file_path": str(output_file_path)}

    except Exception as e:
        return {"status": "generate-failure", "error": str(e)}