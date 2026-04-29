from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv
import re

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
                movility = 'NO ENCONTRADO'
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
                'experience_required': experience,
                'seniority': None,
                'type_contract': contract
            }
            raw_jobs.append(job_data)
        return raw_jobs

    def _safe_extract(self, soup, selector):
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else "N/A"

    def normalize(self, raw_jobs):
        cadena__borrar_movilidad = 'solo '
        cadena_borrar_experiencia = 'experiencia mínima: '
        seniority_map = {
            'junior': ['no requerida', 'al menos 1 año', 'al menos 2 años'],
            'mid': ['al menos 3 años'],
            'senior': ['al menos 4 años', 'al menos 5 años'],
            'architecture': ['más de 5 años']
        }

        for job in raw_jobs:
            raw_exp = job.get('experience_required', '').strip().lower()
            clean_exp = raw_exp.replace(cadena_borrar_experiencia, '').strip().lower()
            raw_movility = job.get('movility', '').strip().lower()
            clean_movility = raw_movility.replace(cadena__borrar_movilidad, '').strip().lower()
            job['experience_required'] = clean_exp.lower()
            job['movility'] = clean_movility.lower()

            salary_raw = job.get('salary', '').strip().lower()
            if 'no disponible' in salary_raw or not salary_raw:
                job['salary'] = None  # Es mejor usar None que 'N/A' para que Pandas lo entienda como vacío
            else:
                # 1. Limpiamos puntos y símbolos para dejar solo números y guiones
                # "17.000€ - 20.000€" -> "17000 - 20000"
                clean_str = salary_raw.replace('.', '').replace('€', '').strip()
                
                # 2. Buscamos el primer bloque de números
                match = re.search(r'\d+', clean_str)
                
                if match:
                    try:
                        # Convertimos el primer número encontrado (ej: 17000)
                        job['salary'] = float(match.group())
                    except ValueError:
                        job['salary'] = None
                else:
                    job['salary'] = None

            found_seniority = 'otro'
            for level, phrases in seniority_map.items():
                if clean_exp in phrases:
                    found_seniority = level
                    break

            job['seniority'] = found_seniority

        return raw_jobs

    def scrape(self):
        html_list = self.fetch()
        raw_jobs = self.parse(html_list)
        normalized_jobs = self.normalize(raw_jobs)
            
        return normalized_jobs