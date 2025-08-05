from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import re

app = Flask(__name__)
CORS(app)

class LinkedInScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_profile(self, profile_url):
        """Scrape LinkedIn profile data"""
        try:
            # Use Selenium for better scraping
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            
            try:
                driver.get(profile_url)
                time.sleep(3)
                
                # Extract profile data
                profile_data = {
                    'name': '',
                    'headline': '',
                    'location': '',
                    'about': '',
                    'experience': [],
                    'education': [],
                    'skills': [],
                    'contact_info': {}
                }
                
                # Get name
                try:
                    name_element = driver.find_element(By.CSS_SELECTOR, 'h1.text-heading-xlarge')
                    profile_data['name'] = name_element.text.strip()
                except:
                    try:
                        name_element = driver.find_element(By.CSS_SELECTOR, '.text-heading-xlarge')
                        profile_data['name'] = name_element.text.strip()
                    except:
                        profile_data['name'] = "Nom non trouvé"
                
                # Get headline
                try:
                    headline_element = driver.find_element(By.CSS_SELECTOR, '.text-body-medium.break-words')
                    profile_data['headline'] = headline_element.text.strip()
                except:
                    profile_data['headline'] = "Titre professionnel non trouvé"
                
                # Get location
                try:
                    location_element = driver.find_element(By.CSS_SELECTOR, '.text-body-small.inline.t-black--light.break-words')
                    profile_data['location'] = location_element.text.strip()
                except:
                    profile_data['location'] = "Localisation non trouvée"
                
                # Get about section
                try:
                    about_element = driver.find_element(By.CSS_SELECTOR, '.pv-shared-text-with-see-more')
                    profile_data['about'] = about_element.text.strip()
                except:
                    profile_data['about'] = "Section À propos non trouvée"
                
                # Get experience
                try:
                    experience_section = driver.find_element(By.ID, 'experience')
                    experience_items = experience_section.find_elements(By.CSS_SELECTOR, '.pvs-list__item--line-separated')
                    
                    for item in experience_items[:5]:  # Limit to 5 most recent
                        try:
                            title_element = item.find_element(By.CSS_SELECTOR, '.t-bold span')
                            company_element = item.find_element(By.CSS_SELECTOR, '.t-normal span')
                            duration_element = item.find_element(By.CSS_SELECTOR, '.t-black--light span')
                            
                            experience = {
                                'title': title_element.text.strip(),
                                'company': company_element.text.strip(),
                                'duration': duration_element.text.strip()
                            }
                            profile_data['experience'].append(experience)
                        except:
                            continue
                except:
                    profile_data['experience'] = []
                
                # Get education
                try:
                    education_section = driver.find_element(By.ID, 'education')
                    education_items = education_section.find_elements(By.CSS_SELECTOR, '.pvs-list__item--line-separated')
                    
                    for item in education_items[:3]:  # Limit to 3 most recent
                        try:
                            school_element = item.find_element(By.CSS_SELECTOR, '.t-bold span')
                            degree_element = item.find_element(By.CSS_SELECTOR, '.t-normal span')
                            
                            education = {
                                'school': school_element.text.strip(),
                                'degree': degree_element.text.strip()
                            }
                            profile_data['education'].append(education)
                        except:
                            continue
                except:
                    profile_data['education'] = []
                
                # Get skills
                try:
                    skills_section = driver.find_element(By.ID, 'skills')
                    skill_items = skills_section.find_elements(By.CSS_SELECTOR, '.pvs-list__item--line-separated')
                    
                    for item in skill_items[:10]:  # Limit to 10 skills
                        try:
                            skill_element = item.find_element(By.CSS_SELECTOR, '.t-bold span')
                            profile_data['skills'].append(skill_element.text.strip())
                        except:
                            continue
                except:
                    profile_data['skills'] = []
                
            finally:
                driver.quit()
            
            return profile_data
            
        except Exception as e:
            print(f"Error scraping profile: {str(e)}")
            return None

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#0A66C2')
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#0A66C2')
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6
        ))
    
    def generate_pdf(self, profile_data, filename="linkedin_resume.pdf"):
        """Generate PDF from LinkedIn profile data"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        story = []
        
        # Header with name and headline
        story.append(Paragraph(profile_data.get('name', 'Nom'), self.styles['CustomTitle']))
        story.append(Paragraph(profile_data.get('headline', 'Titre professionnel'), self.styles['BodyText']))
        story.append(Paragraph(profile_data.get('location', 'Localisation'), self.styles['BodyText']))
        story.append(Spacer(1, 20))
        
        # About section
        if profile_data.get('about'):
            story.append(Paragraph("À PROPOS", self.styles['SectionTitle']))
            story.append(Paragraph(profile_data['about'], self.styles['BodyText']))
            story.append(Spacer(1, 12))
        
        # Experience section
        if profile_data.get('experience'):
            story.append(Paragraph("EXPÉRIENCE PROFESSIONNELLE", self.styles['SectionTitle']))
            
            for exp in profile_data['experience']:
                exp_text = f"<b>{exp.get('title', '')}</b><br/>"
                exp_text += f"{exp.get('company', '')}<br/>"
                exp_text += f"<i>{exp.get('duration', '')}</i>"
                story.append(Paragraph(exp_text, self.styles['BodyText']))
                story.append(Spacer(1, 8))
        
        # Education section
        if profile_data.get('education'):
            story.append(Paragraph("FORMATION", self.styles['SectionTitle']))
            
            for edu in profile_data['education']:
                edu_text = f"<b>{edu.get('school', '')}</b><br/>"
                edu_text += f"{edu.get('degree', '')}"
                story.append(Paragraph(edu_text, self.styles['BodyText']))
                story.append(Spacer(1, 8))
        
        # Skills section
        if profile_data.get('skills'):
            story.append(Paragraph("COMPÉTENCES", self.styles['SectionTitle']))
            skills_text = ", ".join(profile_data['skills'])
            story.append(Paragraph(skills_text, self.styles['BodyText']))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_text = f"Généré automatiquement depuis LinkedIn le {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
        story.append(Paragraph(footer_text, self.styles['BodyText']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()
        linkedin_url = data.get('linkedin_url')
        
        if not linkedin_url:
            return jsonify({'error': 'URL LinkedIn requise'}), 400
        
        # Validate LinkedIn URL
        if 'linkedin.com/in/' not in linkedin_url:
            return jsonify({'error': 'URL LinkedIn invalide'}), 400
        
        # Scrape profile
        scraper = LinkedInScraper()
        profile_data = scraper.scrape_profile(linkedin_url)
        
        if not profile_data:
            return jsonify({'error': 'Impossible de récupérer les données du profil'}), 500
        
        # Generate PDF
        pdf_generator = PDFGenerator()
        pdf_buffer = pdf_generator.generate_pdf(profile_data)
        
        # Return PDF as download
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"resume_{profile_data.get('name', 'linkedin').replace(' ', '_')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'Erreur: {str(e)}'}), 500

@app.route('/api/validate-url', methods=['POST'])
def validate_url():
    data = request.get_json()
    url = data.get('url', '')
    
    if 'linkedin.com/in/' in url:
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False, 'message': 'Veuillez entrer une URL LinkedIn valide'})

@app.route('/sitemap.xml')
def sitemap():
    return app.send_static_file('sitemap.xml')

@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 