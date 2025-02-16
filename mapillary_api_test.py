import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class MapillaryAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://graph.mapillary.com"
        self.headers = {
            'Authorization': f'OAuth {access_token}'
        }

    def get_images_by_username(self, username, bbox=None):
        url = f"{self.base_url}/images"
        
        params = {
            'fields': 'id,geometry,thumb_1024_url,captured_at,creator',
            'creator_username': username,
            'limit': 2000
        }
        
        if bbox:
            params['bbox'] = f'{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}'

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def download_image(self, image_url, save_path):
        response = requests.get(image_url)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)

    def process_images(self, username, download_dir="downloads"):
        # Crear directorio si no existe
        os.makedirs(download_dir, exist_ok=True)
        
        try:
            # Obtener imágenes
            result = self.get_images_by_username(username)
            
            print(f"Found {len(result['data'])} images")
            
            # Procesar cada imagen
            for image in result['data']:
                # Crear nombre de archivo con timestamp
                timestamp = datetime.fromtimestamp(image['captured_at']/1000)
                filename = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{image['id']}.jpg"
                save_path = os.path.join(download_dir, filename)
                
                # Descargar imagen
                print(f"Downloading {filename}...")
                self.download_image(image['thumb_1024_url'], save_path)
                
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

# Uso del código
def main():
    token = os.getenv("API_KEY")
    username = "itagui360"
    bbox = [-75.635, 6.150, -75.590, 6.200]  # Ejemplo para Itagüí
    
    api = MapillaryAPI(token)
    api.process_images(username)

if __name__ == "__main__":
    main()