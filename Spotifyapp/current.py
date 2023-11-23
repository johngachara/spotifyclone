currently_playing_url = 'https://api.spotify.com/v1/me/player/currently-playing'
    response3 = requests.get(currently_playing_url,headers=headers).json()
    currents_dictionary = []



    data = response3.get('item','')
    item_data = data.get('album','')
    current_name = item_data.get('name','')
    current_image = item_data.get('images','')[0]
    current_url = current_image.get('url','')
    current_artist_list = item_data.get('artists','')[0]
    current_artist = current_artist_list.get('name','')
    currents_dictionary.append({"name":current_name,"artist_name":current_artist})
    json_data = response3
    json_data2 = json.loads(json_data)
    value_to_check = 'item'
    if value_to_check is not json_data2.values():
