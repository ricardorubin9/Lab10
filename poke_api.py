'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests
import os
import image_lib

script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_info() function
    # Use breakpoints to view returned dictionary
    poke_info = get_pokemon_info("Rockruff")

    download_pokemon_artwork('Rockruff',r'C:\temp')
    return

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object,
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters
    pokemon = str(pokemon).strip().lower()

    # Check if Pokemon name is an empty string
    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return

    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')

    # TODO: Define function that gets a list of all Pokemon names from the PokeAPI
def get_pokemon_names(limit=100000, offset= 0):
    print(f"Getting all pokemon names...", end="")
    params = {
        "limit": limit, 
        "Offset": offset
    }

    resp_msj = requests.get(POKE_API_URL, params=params)

    if resp_msj.status_code == requests.codes.ok:
        print("Retreived Successfully")

        resp_dict = resp_msj.json()
        return [p["name"] for p in resp_dict["results"]]
    else:
        print (f"Failure in gathering the information. \n Status code: {resp_msj.status_code} ({resp_msj.reason})")
        return None
    
    # TODO: Define function that downloads and saves Pokemon artwork

def download_pokemon_artwork(pokemon_name,folder_path='.'):

    poke_info = get_pokemon_info(pokemon_name)

    if poke_info is None:
        return 
        
    #Extract the artwork URL from the info dictionary
    artwork_url = poke_info['sprites']['other']['official-artwork']['front_default']
    if artwork_url is None:
        print(f"No artwork available for {pokemon_name.capitalize()}.")
        return
        
        #Determine the image file path
    file_ext =artwork_url.split('.')[-1]
    image_path = os.path.join(folder_path, f'{pokemon_name}.{file_ext}')

        #Don't download Pokemon artowrk if there already exists one.
    print (f'Downloading artwork for {pokemon_name.capitalize()}...', end= '')
    image_data = image_lib.download_image(artwork_url)

    if image_data is None:
        return
        #save the image file
    if image_lib.save_image_file(image_data, image_path):
        return image_path

if __name__ == '__main__':
    main()