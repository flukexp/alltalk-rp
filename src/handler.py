

from tts_server import setup
from tts_generate import generate
from schemas import INPUT_SCHEMA

import runpod
from runpod.serverless.utils.rp_validator import validate

import wave

# Flag for ensuring setup is only run once
model_loaded = False

async def handler(job):
    
    global model_loaded

    # Lazy initialization within the handler
    if not model_loaded:
        await setup()
        model_loaded = True
        print("Model setup complete.")
    
    """ Handler function that will be used to process jobs. """
    job_input = job['input']

    # Input validation
    validated_input = validate(job_input, INPUT_SCHEMA)

    if 'errors' in validated_input:
        return {"error": validated_input['errors']}
    validated_input = validated_input['validated_input']

    # Generate audio from text
    text_input = validated_input['text_input']
    text_filtering = validated_input['text_filtering']
    character_voice_gen = validated_input['character_voice_gen']
    narrator_enabled = validated_input['narrator_enabled']
    narrator_voice_gen = validated_input['narrator_voice_gen']
    text_not_inside = validated_input['text_not_inside']
    language = validated_input['language']
    output_file_name = validated_input['output_file_name']
    output_file_timestamp = validated_input['output_file_timestamp']
    autoplay = validated_input['autoplay']
    autoplay_volume = validated_input['autoplay_volume']
    
    result = await generate(text_input, text_filtering, character_voice_gen,
                    narrator_enabled, narrator_voice_gen, text_not_inside, language, 
                    output_file_name, output_file_timestamp, autoplay, autoplay_volume)
    
    # Check the result of the generate function
    if result['status'] == 'generate-success':
        output_file_path = result['output_file_path']
        print(f"Generated file path: {output_file_path}")

        # Read wav file from the generated path
        try:
            with wave.open(output_file_path, 'rb') as wav_file:
                # Extract WAV file parameters
                params = wav_file.getparams()
                # Read audio frames
                audio_data = wav_file.readframes(params.nframes)
        except wave.Error as e:
            return {"error": f"Error reading WAV file: {e}"}

        return {"audio_data": audio_data}

    else:
        # Handle failure case
        return {"error": result.get('error', 'Unknown error occurred')}

runpod.serverless.start({"handler": handler})