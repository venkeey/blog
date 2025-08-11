import requests
from bs4 import BeautifulSoup
import time
import json
import csv
from urllib.parse import urljoin, urlparse, unquote
import re

class GrupoVenusScraper:
    def __init__(self, birth_data=None):
        self.session = requests.Session()
        self.base_url = "https://grupovenus.com/"
        self.readings_data = []
        self.birth_data = birth_data or {}
        
        # Set headers to mimic a browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Known anchor patterns based on your examples
        self.known_anchors = [
            'JUPen%204',      # Jupiter in 4th house
            'SATen%2012',     # Saturn in 12th house  
            'JUPSEXMAR',      # Jupiter Sextile Mars
            'JUPCJCMER',      # Jupiter Conjunction Mercury
            'JUPCUAASC',      # Jupiter Square Ascendant
            'VENOPOLUN',      # Venus Opposition Moon
            'VENOPOMC',       # Venus Opposition Midheaven
            'JUPOPOMC',       # Jupiter Opposition Midheaven
        ]
    
    def submit_birth_data(self):
        """Submit birth data to generate personalized readings"""
        if not self.birth_data:
            print("No birth data provided - using default data")
            # Use the data from your screenshot as default
            self.birth_data = {
                'name': 'Ramesh',
                'day': '1',
                'month': 'January',
                'year': '1980',
                'hour': '10',
                'ampm': 'am',
                'minute': '10',
                'gender': 'Male',
                'country': 'Georgia (usa)',
                'city': 'Suwanee',
                'autocomplete': True
            }
        
        print(f"Submitting birth data for: {self.birth_data.get('name', 'Unknown')}")
        
        try:
            # First get the form page - try multiple possible URLs
            form_urls = [
                "https://grupovenus.com/personasi.asp?nue",
                "https://grupovenus.com/personasi.asp", 
                "https://grupovenus.com/info.asp",
                "https://grupovenus.com/"
            ]
            
            form_response = None
            form_url = None
            
            for url in form_urls:
                try:
                    print(f"Trying form URL: {url}")
                    response = self.session.get(url)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    form = soup.find('form')
                    
                    if form:
                        # Check if this looks like the birth data form
                        inputs = form.find_all('input')
                        has_name = any('name' in inp.get('name', '').lower() for inp in inputs if inp.get('name'))
                        has_birth_fields = any(term in response.text.lower() for term in ['birth', 'nacimiento', 'date', 'fecha'])
                        
                        if has_name or has_birth_fields:
                            print(f"Found birth data form at: {url}")
                            form_response = response
                            form_url = url
                            break
                            
                except requests.RequestException:
                    continue
            
            if not form_response:
                print("Could not find birth data form")
                return False
            
            soup = BeautifulSoup(form_response.text, 'html.parser')
            form = soup.find('form')
            
            # Prepare form data
            form_data = self.prepare_birth_form_data(form)
            
            # Submit the form
            action = form.get('action', '')
            if action:
                if action.startswith('http'):
                    submit_url = action
                elif action.startswith('/'):
                    submit_url = urljoin(self.base_url, action)
                else:
                    submit_url = urljoin(form_url, action)
            else:
                submit_url = form_url
            
            print(f"Submitting birth data to: {submit_url}")
            
            # Add extra headers that might be expected
            headers = {
                'Referer': form_url,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = self.session.post(submit_url, data=form_data, headers=headers, allow_redirects=True)
            response.raise_for_status()
            
            print(f"Form submitted. Final URL: {response.url}")
            print(f"Response status: {response.status_code}")
            
            # Check if we got redirected to the reports page or if response contains report indicators
            success_indicators = ['informes', 'reports', 'jupiter', 'venus', 'mars', 'aspectos', 'aspects']
            if any(indicator in response.url.lower() or indicator in response.text.lower() for indicator in success_indicators):
                print("Birth data submitted successfully - detected astrological content")
                return True
            else:
                print("Birth data submission completed - status unclear")
                # Even if unclear, continue anyway
                return True
                
        except requests.RequestException as e:
            print(f"Error submitting birth data: {e}")
            return False
    
    def prepare_birth_form_data(self, form):
        """Prepare form data from birth information"""
        form_data = {}
        
        # Get all form inputs and their current values
        inputs = form.find_all(['input', 'select', 'textarea'])
        
        for inp in inputs:
            name = inp.get('name')
            if not name:
                continue
            
            inp_type = inp.get('type', '').lower()
            
            # Handle different input types
            if inp_type == 'hidden':
                form_data[name] = inp.get('value', '')
            elif inp_type == 'text':
                # Map text inputs to birth data
                name_lower = name.lower()
                if 'name' in name_lower or 'nombre' in name_lower:
                    form_data[name] = self.birth_data.get('name', 'Ramesh')
                elif 'city' in name_lower or 'ciudad' in name_lower:
                    form_data[name] = self.birth_data.get('city', 'Suwanee')
                elif 'day' in name_lower or 'dia' in name_lower:
                    form_data[name] = self.birth_data.get('day', '1')
                elif 'year' in name_lower or 'ano' in name_lower:
                    form_data[name] = self.birth_data.get('year', '1980')
                elif 'hour' in name_lower or 'hora' in name_lower:
                    form_data[name] = self.birth_data.get('hour', '10')
                elif 'minute' in name_lower or 'minuto' in name_lower:
                    form_data[name] = self.birth_data.get('minute', '10')
                else:
                    form_data[name] = inp.get('value', '')
            elif inp_type == 'radio':
                # Handle gender radio buttons
                if 'gender' in name.lower() or 'sexo' in name.lower():
                    value = inp.get('value', '')
                    gender = self.birth_data.get('gender', 'Male').lower()
                    if (gender == 'male' and value.lower() in ['male', 'm', 'masculino']) or \
                       (gender == 'female' and value.lower() in ['female', 'f', 'femenino']):
                        form_data[name] = value
            elif inp_type == 'checkbox':
                # Handle autocomplete checkbox
                if 'autocomplete' in name.lower():
                    if self.birth_data.get('autocomplete', True):
                        form_data[name] = inp.get('value', 'on')
            elif inp_type == 'submit':
                form_data[name] = inp.get('value', 'Continue')
        
        # Handle select dropdowns
        selects = form.find_all('select')
        for select in selects:
            name = select.get('name')
            if not name:
                continue
            
            name_lower = name.lower()
            if 'month' in name_lower or 'mes' in name_lower:
                form_data[name] = self.birth_data.get('month', 'January')
            elif 'country' in name_lower or 'pais' in name_lower:
                form_data[name] = self.birth_data.get('country', 'Georgia (usa)')
            elif 'ampm' in name_lower:
                form_data[name] = self.birth_data.get('ampm', 'am')
            else:
                # Use first option as default
                options = select.find_all('option')
                if options:
                    form_data[name] = options[0].get('value', '')
        
        print(f"Form data prepared: {list(form_data.keys())}")
        return form_data
        """Find and analyze login forms on the page"""
        forms = soup.find_all('form')
        login_forms = []
        
        for form in forms:
            # Look for forms that might be login forms
            inputs = form.find_all('input')
            has_username = False
            has_password = False
            
            for inp in inputs:
                inp_type = inp.get('type', '').lower()
                inp_name = inp.get('name', '').lower()
                inp_id = inp.get('id', '').lower()
                
                # Check for username/email fields
                if (inp_type in ['text', 'email'] or 
                    any(term in inp_name for term in ['user', 'login', 'email', 'usuario']) or
                    any(term in inp_id for term in ['user', 'login', 'email', 'usuario'])):
                    has_username = True
                
                # Check for password fields
                if (inp_type == 'password' or 
                    any(term in inp_name for term in ['pass', 'pwd', 'contraseña']) or
                    any(term in inp_id for term in ['pass', 'pwd', 'contraseña'])):
                    has_password = True
            
            if has_username and has_password:
                login_forms.append(form)
                print(f"Found potential login form with action: {form.get('action', 'No action')}")
        
        return login_forms
    
    def attempt_login(self):
        """Attempt to login to the site"""
        if not self.username or not self.password:
            print("No login credentials provided")
            return False
        
        print(f"Attempting login with username: {self.username}")
        
        # First, get the main page to find login forms
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for login forms
            login_forms = self.find_login_form(soup)
            
            if not login_forms:
                # Try common login page URLs
                login_urls = [
                    'login.asp', 'login.php', 'signin.asp', 'signin.php',
                    'acceso.asp', 'acceso.php', 'entrar.asp', 'entrar.php'
                ]
                
                for login_url in login_urls:
                    try:
                        full_url = urljoin(self.base_url, login_url)
                        print(f"Trying login page: {full_url}")
                        response = self.session.get(full_url)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, 'html.parser')
                            login_forms = self.find_login_form(soup)
                            if login_forms:
                                print(f"Found login form at: {full_url}")
                                break
                    except:
                        continue
            
            if not login_forms:
                print("No login forms found on the site")
                return False
            
            # Try to login with the first form found
            form = login_forms[0]
            return self.submit_login_form(form, response.url)
            
        except requests.RequestException as e:
            print(f"Error during login attempt: {e}")
            return False
    
    def submit_login_form(self, form, current_url):
        """Submit login credentials to a form"""
        action = form.get('action')
        method = form.get('method', 'POST').upper()
        
        # Build the form submission URL
        if action:
            if action.startswith('http'):
                form_url = action
            else:
                form_url = urljoin(current_url, action)
        else:
            form_url = current_url
        
        print(f"Submitting login to: {form_url}")
        
        # Collect all form data
        form_data = {}
        
        inputs = form.find_all(['input', 'select', 'textarea'])
        for inp in inputs:
            name = inp.get('name')
            if not name:
                continue
                
            inp_type = inp.get('type', '').lower()
            inp_name_lower = name.lower()
            
            # Handle different input types
            if inp_type == 'hidden':
                form_data[name] = inp.get('value', '')
            elif inp_type == 'password' or 'pass' in inp_name_lower:
                form_data[name] = self.password
            elif (inp_type in ['text', 'email'] or 
                  any(term in inp_name_lower for term in ['user', 'login', 'email', 'usuario'])):
                form_data[name] = self.username
            elif inp_type == 'submit':
                form_data[name] = inp.get('value', 'Submit')
            elif inp_type == 'checkbox':
                # Usually leave unchecked unless specified
                pass
            else:
                # For other input types, use default value if available
                default_value = inp.get('value', '')
                if default_value:
                    form_data[name] = default_value
        
        print(f"Form data keys: {list(form_data.keys())}")
        
        try:
            if method == 'GET':
                response = self.session.get(form_url, params=form_data)
            else:
                response = self.session.post(form_url, data=form_data)
            
            response.raise_for_status()
            
            # Check if login was successful
            if self.check_login_success(response):
                print("Login successful!")
                return True
            else:
                print("Login appears to have failed")
                return False
                
        except requests.RequestException as e:
            print(f"Error submitting login form: {e}")
            return False
    
    def check_login_success(self, response):
        """Check if login was successful by analyzing the response"""
        # Common indicators of successful login
        success_indicators = [
            'bienvenido', 'welcome', 'dashboard', 'logout', 'cerrar sesión',
            'mi cuenta', 'my account', 'perfil', 'profile'
        ]
        
        # Common indicators of failed login
        failure_indicators = [
            'error', 'incorrecto', 'incorrect', 'invalid', 'failed',
            'usuario o contraseña', 'username or password', 'login failed'
        ]
        
        response_text = response.text.lower()
        
        # Check for failure indicators first
        for indicator in failure_indicators:
            if indicator in response_text:
                print(f"Login failure indicator found: {indicator}")
                return False
        
        # Check for success indicators
        for indicator in success_indicators:
            if indicator in response_text:
                print(f"Login success indicator found: {indicator}")
                return True
        
        # If redirected to a different page, might be successful
        if len(response.history) > 0:
            print("Redirected after login - likely successful")
            return True
        
        # Try to access a protected page to confirm
        try:
            test_response = self.session.get(urljoin(self.base_url, "informes3.asp"))
            if "Sesión ha caducado" not in test_response.text and "Session expired" not in test_response.text:
                print("Can access protected content - login successful")
                return True
        except:
            pass
        
        print("Login status unclear - proceeding with caution")
        return True  # Assume success if we can't determine otherwise
        """Initialize session by visiting the main page"""
        try:
            print("Starting session...")
            response = self.session.get(self.base_url)
            response.raise_for_status()
            print(f"Session started. Status code: {response.status_code}")
            return True
        except requests.RequestException as e:
            print(f"Error starting session: {e}")
            return False
    
    def get_informes_page(self):
        """Try to access the informes3.asp page with retry logic"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                print(f"Accessing informes3.asp... (attempt {retry_count + 1}/{max_retries})")
                url = urljoin(self.base_url, "informes3.asp")
                response = self.session.get(url)
                response.raise_for_status()
                
                # Check if we got the session expired message
                if "Sesión ha caducado" in response.text or "Session expired" in response.text:
                    print(f"Session expired on attempt {retry_count + 1}")
                    
                    if retry_count < max_retries - 1:  # Don't retry on last attempt
                        result = self.handle_session_expired(response)
                        if result:
                            return result
                        retry_count += 1
                        time.sleep(3)  # Wait longer between retries
                        continue
                    else:
                        print("Max retries reached - session handling failed")
                        return None
                
                print("Successfully accessed informes3.asp")
                return response
                
            except requests.RequestException as e:
                print(f"Error accessing informes page (attempt {retry_count + 1}): {e}")
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(2)
                    continue
                else:
                    return None
        
        return None
    
    def handle_session_expired(self, response):
        """Handle session expiration by following the reinit link and submitting birth data"""
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for reinitiation links
        reinit_links = soup.find_all('a', href=True)
        for link in reinit_links:
            link_text = link.text.lower()
            if any(word in link_text for word in ['aquí', 'here', 'ici', 'clique']):
                reinit_url = urljoin(self.base_url, link['href'])
                print(f"Following reinit link: {reinit_url}")
                
                try:
                    response = self.session.get(reinit_url)
                    response.raise_for_status()
                    time.sleep(2)  # Wait a bit after reinitializing
                    
                    # After reinitializing, submit birth data again to establish proper session
                    print("Re-submitting birth data after session reinit...")
                    if self.submit_birth_data():
                        print("Birth data re-submitted successfully")
                        time.sleep(2)  # Wait for processing
                        
                        # Now try to access informes3.asp again  
                        return self.get_informes_page()
                    else:
                        print("Failed to re-submit birth data")
                        return None
                        
                except requests.RequestException as e:
                    print(f"Error following reinit link: {e}")
                    return None
        
        print("Could not find reinitiation link")
        return None
    
    def extract_anchor_links(self, soup):
        """Extract all anchor links that point to readings on the same page"""
        anchors = set()
        
        # Look for links with # fragments pointing to informes3.asp
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            if href and '#' in href:
                # Check if it's pointing to informes3.asp or is a relative anchor
                if 'informes3.asp#' in href or href.startswith('#'):
                    # Extract the anchor part
                    anchor = href.split('#')[-1]
                    if anchor:
                        anchors.add(anchor)
                        print(f"Found anchor: {anchor} (from link: {link.get_text(strip=True)})")
        
        # Also look for JavaScript code that might reference anchors
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Look for anchor patterns in JavaScript
                anchor_matches = re.findall(r'#([A-Z0-9%]+)', script.string)
                for match in anchor_matches:
                    anchors.add(match)
                    print(f"Found anchor in script: {match}")
        
        # Add known anchors from examples
        for known_anchor in self.known_anchors:
            anchors.add(known_anchor)
        
        return list(anchors)
    
    def generate_comprehensive_anchor_list(self):
        """Generate a comprehensive list of possible anchors based on astrological patterns"""
        anchors = []
        
        # Planet codes (including alternative notations)
        planets = ['SOL', 'LUN', 'MER', 'VEN', 'MAR', 'JUP', 'SAT', 'URA', 'NEP', 'PLU']
        # Alternative planet codes that might be used
        planet_alts = {
            'LUN': ['LUNA'],  # Moon alternatives
        }
        
        # House numbers (1-12)
        houses = range(1, 13)
        
        # Aspect codes
        aspects = {
            'CJC': 'Conjunction',
            'SEX': 'Sextile', 
            'CUA': 'Square',
            'TRI': 'Trine',
            'OPO': 'Opposition',
            'QUIN': 'Quincunx'
        }
        
        # Special points
        special_points = ['ASC', 'MC', 'NOD']
        
        # Generate planet in house combinations
        for planet in planets:
            for house in houses:
                # Format: PLANETen HOUSE (en = "en" = "in")
                anchor = f"{planet}en%20{house}"
                anchors.append({
                    'anchor': anchor,
                    'description': f"{planet} in House {house}",
                    'type': 'house_position'
                })
        
        # Generate planet-planet aspects
        for i, planet1 in enumerate(planets):
            for planet2 in planets[i+1:]:  # Avoid duplicates
                for aspect_code, aspect_name in aspects.items():
                    anchor = f"{planet1}{aspect_code}{planet2}"
                    anchors.append({
                        'anchor': anchor,
                        'description': f"{planet1} {aspect_name} {planet2}",
                        'type': 'planet_aspect'
                    })
        
        # Generate planet-special point aspects
        for planet in planets:
            for special in special_points:
                for aspect_code, aspect_name in aspects.items():
                    anchor = f"{planet}{aspect_code}{special}"
                    anchors.append({
                        'anchor': anchor,
                        'description': f"{planet} {aspect_name} {special}",
                        'type': 'special_aspect'
                    })
        
        return anchors
    
    def extract_reading_by_anchor(self, soup, anchor_id):
        """Extract reading content for a specific anchor"""
        # Look for elements with the anchor ID
        target_element = soup.find(id=anchor_id)
        if target_element:
            return self.extract_text_content(target_element)
        
        # If not found by ID, look for anchor tags
        anchor_link = soup.find('a', {'name': anchor_id})
        if anchor_link:
            # Get content after the anchor
            content = []
            for sibling in anchor_link.find_next_siblings():
                if sibling.name == 'a' and sibling.get('name'):
                    # Stop at next anchor
                    break
                content.append(self.extract_text_content(sibling))
            return '\n'.join(content)
        
        # Look for content in divs or other containers that might contain the anchor
        # Sometimes content is organized in sections
        all_text = soup.get_text()
        if anchor_id in all_text or unquote(anchor_id) in all_text:
            # Try to extract content around the anchor reference
            lines = all_text.split('\n')
            anchor_decoded = unquote(anchor_id)
            
            for i, line in enumerate(lines):
                if anchor_id in line or anchor_decoded in line:
                    # Extract several lines after finding the anchor reference
                    start_idx = max(0, i-2)
                    end_idx = min(len(lines), i+20)  # Get ~20 lines of content
                    return '\n'.join(lines[start_idx:end_idx]).strip()
        
        return None
    
    def extract_text_content(self, element):
        """Extract clean text content from an element"""
        if not element:
            return ""
        
        # Remove script and style elements
        for script in element.find_all(["script", "style"]):
            script.decompose()
        
        # Get text and clean it up
        text = element.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in chunks if chunk)
    
    def scrape_all_readings(self):
        """Main method to scrape all readings"""
        # Start session by submitting birth data
        if not self.submit_birth_data():
            return False
        
        # Get the main informes page
        response = self.get_informes_page()
        if not response:
            print("Could not access informes page")
            return False
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract anchor links found in the page
        found_anchors = self.extract_anchor_links(soup)
        print(f"Found {len(found_anchors)} anchors in the page")
        
        # Generate comprehensive list of possible anchors
        comprehensive_anchors = self.generate_comprehensive_anchor_list()
        print(f"Generated {len(comprehensive_anchors)} possible anchors based on astrological patterns")
        
        # Combine found anchors with comprehensive list
        all_anchors_to_try = found_anchors.copy()
        for comp_anchor in comprehensive_anchors:
            if comp_anchor['anchor'] not in all_anchors_to_try:
                all_anchors_to_try.append(comp_anchor['anchor'])
        
        print(f"Total anchors to try: {len(all_anchors_to_try)}")
        
        # Try to extract content for each anchor
        successful_extractions = 0
        for i, anchor in enumerate(all_anchors_to_try):
            if isinstance(anchor, dict):
                anchor_id = anchor['anchor']
                description = anchor.get('description', anchor_id)
                anchor_type = anchor.get('type', 'unknown')
            else:
                anchor_id = anchor
                description = unquote(anchor_id)
                anchor_type = 'found_in_page'
            
            print(f"Processing anchor {i+1}/{len(all_anchors_to_try)}: {anchor_id}")
            
            content = self.extract_reading_by_anchor(soup, anchor_id)
            if content and len(content.strip()) > 50:  # Only save if we got substantial content
                self.readings_data.append({
                    'anchor': anchor_id,
                    'description': description,
                    'type': anchor_type,
                    'url': f"https://grupovenus.com/informes3.asp#{anchor_id}",
                    'content': content.strip()
                })
                successful_extractions += 1
                print(f"  ✓ Extracted content ({len(content)} characters)")
            else:
                print(f"  ✗ No content found")
            
            # Small delay to be respectful
            if i % 50 == 0 and i > 0:  # Longer pause every 50 attempts
                time.sleep(2)
            else:
                time.sleep(0.1)
        
        print(f"\nExtraction completed: {successful_extractions} successful extractions out of {len(all_anchors_to_try)} attempts")
        return True
    
    def save_readings_to_json(self, filename='venus_readings.json'):
        """Save all readings to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.readings_data, f, indent=2, ensure_ascii=False)
        print(f"Readings saved to {filename}")
    
    def save_readings_to_csv(self, filename='venus_readings.csv'):
        """Save all readings to a CSV file"""
        if not self.readings_data:
            print("No readings to save")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['anchor', 'description', 'type', 'url', 'content']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.readings_data)
        print(f"Readings saved to {filename}")
    
    def print_summary(self):
        """Print a summary of extracted readings"""
        if not self.readings_data:
            print("No readings were extracted")
            return
        
        print(f"\n=== EXTRACTION SUMMARY ===")
        print(f"Total readings extracted: {len(self.readings_data)}")
        
        # Group by type
        by_type = {}
        for reading in self.readings_data:
            reading_type = reading['type']
            if reading_type not in by_type:
                by_type[reading_type] = []
            by_type[reading_type].append(reading)
        
        for reading_type, readings in by_type.items():
            print(f"\n{reading_type.upper()} ({len(readings)} readings):")
            for reading in readings[:5]:  # Show first 5 of each type
                print(f"  - {reading['description']}: {len(reading['content'])} chars")
            if len(readings) > 5:
                print(f"  ... and {len(readings) - 5} more")

def get_birth_data_from_user():
    """Get birth data from user input"""
    print("=== Birth Data Input ===")
    print("Enter birth details for personalized astrological readings:")
    
    birth_data = {}
    
    birth_data['name'] = input("Name (default: Ramesh): ").strip() or "Ramesh"
    
    # Birth date
    birth_data['day'] = input("Birth day (1-31, default: 1): ").strip() or "1"
    
    print("Birth month:")
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    for i, month in enumerate(months, 1):
        print(f"{i}. {month}")
    month_choice = input("Enter month number (1-12, default: 1): ").strip() or "1"
    try:
        month_idx = int(month_choice) - 1
        birth_data['month'] = months[month_idx] if 0 <= month_idx < 12 else "January"
    except ValueError:
        birth_data['month'] = "January"
    
    birth_data['year'] = input("Birth year (default: 1980): ").strip() or "1980"
    
    # Birth time
    birth_data['hour'] = input("Birth hour (1-12, default: 10): ").strip() or "10"
    birth_data['minute'] = input("Birth minute (0-59, default: 10): ").strip() or "10"
    ampm = input("AM or PM? (default: AM): ").strip().lower()
    birth_data['ampm'] = "am" if ampm in ['am', 'a', ''] else "pm"
    
    # Gender
    gender = input("Gender (M/F, default: M): ").strip().lower()
    birth_data['gender'] = "Male" if gender in ['m', 'male', ''] else "Female"
    
    # Location
    birth_data['country'] = input("Country (default: Georgia (usa)): ").strip() or "Georgia (usa)"
    birth_data['city'] = input("City of birth (default: Suwanee): ").strip() or "Suwanee"
    
    birth_data['autocomplete'] = True
    
    return birth_data

def main():
    print("=== Grupo Venus Astrological Reports Scraper ===")
    
    # Ask if user wants to input custom birth data
    use_custom = input("Do you want to enter custom birth data? (y/N): ").strip().lower()
    
    if use_custom in ['y', 'yes']:
        birth_data = get_birth_data_from_user()
        scraper = GrupoVenusScraper(birth_data)
    else:
        print("Using default birth data from screenshot (Ramesh, Jan 1 1980, 10:10 AM, Suwanee GA)")
        scraper = GrupoVenusScraper()
    
    print("\nStarting Grupo Venus anchor-based scraper...")
    success = scraper.scrape_all_readings()
    
    if success:
        scraper.print_summary()
        
        # Save results
        scraper.save_readings_to_json()
        scraper.save_readings_to_csv()
        
        print(f"\nAll data saved. Check venus_readings.json and venus_readings.csv")
    else:
        print("Scraping failed. Check the error messages above.")

if __name__ == "__main__":
    main()
