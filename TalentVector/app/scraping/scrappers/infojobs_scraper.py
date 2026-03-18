from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv

class InfoJobsScraper:
    url_listado = os.getenv('URL_SCRAP')
    def __init__(self):
        load_dotenv()
        self.url_listado = os.getenv('URL_SCRAP')
        if not self.url_listado:
            raise ValueError('Error: No se encontró URL_SCRAP en el archivo de configuración.')

    def fetch(self):
        data_list = []
        with sync_playwright() as p:
            # Usamos launch_persistent_context para guardar cookies y parecer más humanos
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 720}
            )
            page = context.new_page()
            
            print("Accediendo al listado...")
            page.goto(self.url_listado, wait_until="networkidle")
            
            # Gestionar cookies UNA SOLA VEZ
            try:
                page.wait_for_selector('#didomi-notice-agree-button', timeout=8000)
                page.click('#didomi-notice-agree-button')
                time.sleep(2)
            except:
                print("Banner de cookies no detectado, continuando...")


            # Extraer URLs
            page.wait_for_selector('.ij-OfferCardContent-description-title', timeout=10000)
            links = page.locator('.ij-OfferCardContent-description-title a')
            urls = [links.nth(i).get_attribute('href') for i in range(min(links.count(), 10))]

            for url in urls:
                full_url = url if url.startswith('http') else f"https:{url}"
                print(f"Navegando a: {full_url}")
                
                try:
                    # Navegación con timeout más largo y espera a carga completa
                    page.goto(full_url, wait_until="domcontentloaded", timeout=60000)
                    
                    # INTENTO DE RE-ACEPTAR COOKIES (A veces reaparecen en el detalle)
                    if page.locator('#didomi-notice-agree-button').is_visible():
                        page.click('#didomi-notice-agree-button')

                    # Esperamos a CUALQUIER contenido relevante, no solo la descripción
                    # Si esto falla, sacamos captura para ver el error
                    try:
                        page.wait_for_selector('h1', timeout=10000) 
                        data_list.append({
                            'url': full_url,
                            'html': page.content()
                        })
                    except:
                        page.screenshot(path=f"error_captura_{int(time.time())}.png")
                    
                    time.sleep(3) # Pausa más larga entre ofertas
                except Exception as e:
                    print(f"Error crítico en {full_url}: {e}")
            
            browser.close()
        return data_list

    def parse(self, data_list):
        raw_jobs = []
        for item in data_list:
            url_oferta = item['url']
            html = item['html']
            soup = BeautifulSoup(html, 'html.parser')

            # 1. Restringimos la búsqueda al contenedor específico
            contenedor_detalles = soup.select_one('.ij-Box.ij-OfferDetailHeader-detailsList')
            
            if not contenedor_detalles:
                continue # Saltamos si no encontramos el encabezado

            # 2. Buscamos los párrafos SOLO dentro de ese contenedor
            elementos_base = contenedor_detalles.select('p.ij-BaseTypography.ij-Text.ij-Text-body1')
            num_elem = len(elementos_base)

            elementos_descripcion = soup.select('.ij-Box.mb-xl.mt-l')

            if num_elem == 5:
                location = elementos_base[0].get_text()
                movility = elementos_base[1].get_text()
                salary = elementos_base[2].get_text()
                experience = elementos_base[3].get_text()
                contract = elementos_base[4].get_text()
            elif num_elem == 4:
                location = elementos_base[0].get_text()
                salary = elementos_base[1].get_text()
                experience = elementos_base[2].get_text()
                contract = elementos_base[3].get_text()
            else:
                location = 'NO ENCONTRADO'
                movility = 'NO ENCONTRADO'
                salary = 'NO ENCONTRADO'
                experience = 'NO ENCONTRADO'
                contract = 'NO ENCONTRADO'

            img_element = soup.select_one('img.sui-AtomImage-image')

            logo_url = img_element['src'] if img_element and img_element.has_attr('src') else 'N/A'
            
            
            # Selectores actualizados para la página de DETALLE de InfoJobs
            job_data = {
                'url' : url_oferta,
                'title': self._safe_extract(soup, 'h1'),
                'company': self._safe_extract(soup, 'a.ij-Link.ij-BaseTypography.ij-BaseTypography-primary.ij-Heading.ij-Heading-headline2'),
                'image': logo_url,
                'location': location,
                'movility': movility,
                'salary': salary,
                'description': '\n'.join([elem.get_text() for elem in elementos_descripcion]),
                'skills': [tag.text.strip() for tag in soup.select('a.sui-AtomTag-actionable.sui-AtomTag.sui-AtomTag--size-m.sui-AtomTag--design-outline.sui-AtomTag--color-primary.sui-AtomTag-hasIcon')],
                'seniority': experience,
                'type_contract': contract
            }
            raw_jobs.append(job_data)
        return raw_jobs

    def _safe_extract(self, soup, selector):
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else "N/A"

    def normalize(self, raw_jobs):
        # Aquí puedes limpiar los datos (quitar símbolos de moneda, normalizar fechas, etc.)
        return [job for job in raw_jobs]

    def scrape(self):
        # print("Iniciando captación de ofertas...")
        html_list = self.fetch()
        # print(f"Páginas descargadas: {len(html_list)}. Parseando...")
        raw_jobs = self.parse(html_list)
        normalized_jobs = self.normalize(raw_jobs)
            
        return normalized_jobs