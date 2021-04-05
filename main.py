def hello_world(request):

    #inputs requires
    #message example gs:// link
    #uuid

    from google.cloud import texttospeech
    from google.cloud import storage
    import re
    import os

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\gcp_credentials\elaborate-howl-285701-105c2e8355a8.json"

    client = texttospeech.TextToSpeechClient()
    storage_client = storage.Client()

    request_json = request.get_json()
    request_json and 'message' in request_json
    link=request_json['message']
    print(link)

    try:

        request_json and 'uuid' in request_json#in case of uuid present
        uuid=request_json['uuid']
        print(uuid)
    except:#in case of uuid not present
        
        import uuid
        uuid=str(uuid.uuid1())
        print(uuid)

    request_json and 'audio_dest' in request_json
    audio_dest=request_json['audio_dest']
    print(audio_dest)


    
    

    match = re.match(r'gs://([^/]+)/(.+)', link)
    prefix = match.group(2)
    bucket = match.group(1)
    real_name=re.split("[/]",prefix)
    real_name=real_name[-1]
  
    print(real_name)
    real_name=re.sub(".txt",".mp3",real_name)
    print(real_name)
    
    
    #x = re.sub("[.]pdf", "_result.txt", prefix)

    bucket = storage_client.bucket(bucket)#should be variable should tell in post request
    blob = bucket.blob(prefix)
    txt_to_convert=blob.download_as_string()
    print(txt_to_convert)

    input_text = texttospeech.SynthesisInput(text=txt_to_convert)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    #audio_result="/tmp/"+uuid+real_name #for cloud function
    audio_result=uuid+real_name


    with open(audio_result, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    
    destination_name=audio_dest+"/MP3/"+uuid+"_"+real_name
    blob = bucket.blob(destination_name)
    blob.upload_from_filename(audio_result)


    
    #input_text = texttospeech.SynthesisInput(text=text)



    return destination_name
   
