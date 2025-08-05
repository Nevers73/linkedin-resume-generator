from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import time
import re
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

class LinkedInScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def extract_profile_data(self, linkedin_url):
        """Extrait les données du profil LinkedIn en utilisant requests + BeautifulSoup"""
        try:
            # Validation de l'URL
            if not self._validate_linkedin_url(linkedin_url):
                return {"error": "URL LinkedIn invalide"}
            
            # Récupération de la page
            response = self.session.get(linkedin_url, timeout=10)
            response.raise_for_status()
            
            # Parsing avec BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraction des données
            profile_data = {
                "name": self._extract_name(soup),
                "headline": self._extract_headline(soup),
                "location": self._extract_location(soup),
                "about": self._extract_about(soup),
                "experience": self._extract_experience(soup),
                "education": self._extract_education(soup),
                "skills": self._extract_skills(soup),
                "url": linkedin_url
            }
            
            # Vérification si les données sont valides
            if not profile_data["name"]:
                return {"error": "Profil privé ou données non accessibles. Assurez-vous que votre profil LinkedIn est public."}
            
            return profile_data
            
        except requests.RequestException as e:
            return {"error": f"Erreur de connexion: {str(e)}"}
        except Exception as e:
            return {"error": f"Erreur lors de l'extraction: {str(e)}"}
    
    def _validate_linkedin_url(self, url):
        """Valide l'URL LinkedIn"""
        try:
            parsed = urlparse(url)
            return 'linkedin.com' in parsed.netloc and '/in/' in parsed.path
        except:
            return False
    
    def _extract_name(self, soup):
        """Extrait le nom du profil"""
        # Plusieurs sélecteurs possibles pour le nom
        selectors = [
            'h1.text-heading-xlarge',
            '.text-heading-xlarge',
            'h1[class*="headline"]',
            '.pv-text-details__left-panel h1',
            '.profile-background-image__image h1'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "Nom non trouvé"
    
    def _extract_headline(self, soup):
        """Extrait le titre professionnel"""
        selectors = [
            '.text-body-medium.break-words',
            '.pv-text-details__left-panel .text-body-medium',
            '.profile-background-image__image .text-body-medium'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "Titre professionnel non trouvé"
    
    def _extract_location(self, soup):
        """Extrait la localisation"""
        selectors = [
            '.text-body-small.inline.t-black--light.break-words',
            '.pv-text-details__left-panel .text-body-small',
            '[data-section="location"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "Localisation non trouvée"
    
    def _extract_about(self, soup):
        """Extrait la section À propos"""
        selectors = [
            '#about ~ .display-flex .inline-show-more-text',
            '.pv-shared-text-with-see-more .inline-show-more-text',
            '[data-section="summary"] .inline-show-more-text'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "Section À propos non trouvée"
    
    def _extract_experience(self, soup):
        """Extrait l'expérience professionnelle"""
        experience = []
        selectors = [
            '#experience ~ .pvs-list__outer-container .pvs-entity',
            '.experience__item',
            '[data-section="experience"] .pvs-entity'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements[:5]:  # Limite à 5 expériences
                exp = self._parse_experience_item(element)
                if exp:
                    experience.append(exp)
        
        return experience if experience else [{"title": "Expérience non trouvée", "company": "", "duration": ""}]
    
    def _parse_experience_item(self, element):
        """Parse un élément d'expérience"""
        try:
            title_elem = element.select_one('.t-bold span, .pvs-entity__path-node span')
            company_elem = element.select_one('.t-normal span, .pvs-entity__path-node + span')
            duration_elem = element.select_one('.pvs-entity__caption-wrapper span')
            
            title = title_elem.get_text(strip=True) if title_elem else "Titre non trouvé"
            company = company_elem.get_text(strip=True) if company_elem else "Entreprise non trouvée"
            duration = duration_elem.get_text(strip=True) if duration_elem else "Durée non trouvée"
            
            return {"title": title, "company": company, "duration": duration}
        except:
            return None
    
    def _extract_education(self, soup):
        """Extrait l'éducation"""
        education = []
        selectors = [
            '#education ~ .pvs-list__outer-container .pvs-entity',
            '.education__item',
            '[data-section="education"] .pvs-entity'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements[:3]:  # Limite à 3 formations
                edu = self._parse_education_item(element)
                if edu:
                    education.append(edu)
        
        return education if education else [{"school": "Formation non trouvée", "degree": "", "year": ""}]
    
    def _parse_education_item(self, element):
        """Parse un élément d'éducation"""
        try:
            school_elem = element.select_one('.t-bold span, .pvs-entity__path-node span')
            degree_elem = element.select_one('.t-normal span, .pvs-entity__path-node + span')
            year_elem = element.select_one('.pvs-entity__caption-wrapper span')
            
            school = school_elem.get_text(strip=True) if school_elem else "École non trouvée"
            degree = degree_elem.get_text(strip=True) if degree_elem else "Diplôme non trouvé"
            year = year_elem.get_text(strip=True) if year_elem else "Année non trouvée"
            
            return {"school": school, "degree": degree, "year": year}
        except:
            return None
    
    def _extract_skills(self, soup):
        """Extrait les compétences"""
        skills = []
        selectors = [
            '#skills ~ .pvs-list__outer-container .pvs-entity',
            '.skill-categories-entities .pvs-entity',
            '[data-section="skills"] .pvs-entity'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements[:10]:  # Limite à 10 compétences
                skill = self._parse_skill_item(element)
                if skill:
                    skills.append(skill)
        
        return skills if skills else ["Compétences non trouvées"]

    def _parse_skill_item(self, element):
        """Parse un élément de compétence"""
        try:
            skill_elem = element.select_one('.t-bold span, .pvs-entity__path-node span')
            return skill_elem.get_text(strip=True) if skill_elem else None
        except:
            return None
    
    def generate_sample_data(self, linkedin_url):
        """Génère des données d'exemple pour les profils privés"""
        return {
            "name": "Exemple de Profil",
            "headline": "Développeur Full Stack | Expert en Python & JavaScript",
            "location": "Paris, France",
            "about": "Développeur passionné avec 5+ années d'expérience dans le développement web. Spécialisé dans les technologies modernes et l'optimisation des performances.",
            "experience": [
                {"title": "Développeur Full Stack Senior", "company": "TechCorp", "duration": "2022 - Présent"},
                {"title": "Développeur Backend", "company": "StartupXYZ", "duration": "2020 - 2022"},
                {"title": "Développeur Junior", "company": "DigitalAgency", "duration": "2019 - 2020"}
            ],
            "education": [
                {"school": "École d'Ingénieurs", "degree": "Master en Informatique", "year": "2019"},
                {"school": "Université de Paris", "degree": "Licence en Mathématiques", "year": "2017"}
            ],
            "skills": ["Python", "JavaScript", "React", "Node.js", "Django", "PostgreSQL", "Docker", "AWS", "Git", "Agile"],
            "url": linkedin_url
        }

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
        linkedin_url = data.get('linkedin_url', '').strip()
        use_sample = data.get('use_sample', False)
        
        if not linkedin_url and not use_sample:
            return jsonify({'error': 'URL LinkedIn requise'}), 400
        
        # Scrape profile
        scraper = LinkedInScraper()
        
        if use_sample:
            # Utiliser des données d'exemple
            profile_data = scraper.generate_sample_data(linkedin_url or "https://linkedin.com/in/exemple")
        else:
            # Essayer de scraper le vrai profil
            profile_data = scraper.extract_profile_data(linkedin_url)
            
            # Si le scraping échoue, proposer les données d'exemple
            if profile_data.get('error'):
                return jsonify({
                    'error': profile_data['error'],
                    'suggestion': 'Utilisez le mode démo avec des données d\'exemple',
                    'use_sample_available': True
                }), 500
        
        if not profile_data:
            return jsonify({'error': 'Impossible de récupérer les données du profil'}), 500
        
        # Generate PDF
        pdf_generator = PDFGenerator()
        pdf_buffer = pdf_generator.generate_pdf(profile_data)
        
        # Return PDF
        pdf_buffer.seek(0)
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"CV_{profile_data['name'].replace(' ', '_')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la génération: {str(e)}'}), 500

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