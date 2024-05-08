import requests
from decouple import config
import re

from django.core.exceptions import ObjectDoesNotExist
from sentence_transformers import SentenceTransformer, util
import numpy as np
from Core.models import UserResume
import fitz
from docx import Document
import textract

class ParsingFunctions:
    def __init__(self):
        self.HF_TOKEN = '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'
        self.API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        self.headers = {"Authorization": f"Bearer {self.HF_TOKEN}"}
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    def query(self, payload):
        try:
            response = requests.post(self.API_URL, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.RequestException as e:
            print(f"Request exception occurred: {e}")
        except Exception as e:
            print(f"Some other error occurred: {e}")
        return []

    def gen_query(self, resume_text):
        payload = {
            "inputs":
                f"""
                Here is a resume detailing various technical experiences and skills. Please analyze the resume and extract the most important technical skills. Focus on identifying specific technologies or tools that are represented as one-word items typical in the tech industry, such as programming languages or widely recognized technology terms.:
                [{resume_text}]
                Please list the top skills demonstrated by this individual as single words that are commonly used as standalone skills in the tech industry.
                """,
            "parameters": {"return_full_text": False, "num_results": 10},
        }
        return self.query(payload)
    def post_processing(self, output):
        text = output[0]['generated_text'] if output else ''
        skills_list = [re.sub(r'^\s*\d+\.\s*', '', line).strip() for line in text.split('\n') if line.strip()]
        print("Extracted Skills:", skills_list)
        with open("Data/SkillsDataSet", 'r') as file:
            skill_dataset = [line.strip() for line in file]
        dataset_embeddings = self.model.encode(skill_dataset)
        extracted_embeddings = self.model.encode(skills_list)
        high_similarity_skills = []
        for skill, embedding in zip(skills_list, extracted_embeddings):
            similarities = util.pytorch_cos_sim(embedding, dataset_embeddings)[0]
            top_indices = np.where(similarities > 0.75)[0]
            if len(top_indices) > 0:
                highest_index = top_indices[np.argmax(similarities[top_indices])]
                high_similarity_skills.append(skill_dataset[highest_index])
        return high_similarity_skills


class ResumeParsing:
    def __init__(self, request):
        self.request = request

    def extract_text_from_pdf(self):
        try:
            resume = UserResume.objects.get(user=self.request.user)
            if not resume.resume:
                return None
            text = ""
            with fitz.open(resume.resume.path) as doc:
                for page in doc:
                    text += page.get_text()
            return text
        except ObjectDoesNotExist:
            print("Resume file does not exist for the user.")
            return None
        except Exception as e:
            print(f"An error occurred while extracting text from PDF: {e}")
            return None

    def extract_text_from_docx(self):
        try:
            resume = UserResume.objects.get(user=self.request.user)
            if not resume.resume:
                return None
            if resume.resume.path.endswith('.docx'):
                doc = Document(resume.resume.path)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                return text
            return None
        except ObjectDoesNotExist:
            print("Resume file does not exist for the user.")
            return None
        except Exception as e:
            print(f"An error occurred while extracting text from DOCX: {e}")
            return None

    def extract_text_from_doc(self):
        try:
            resume = UserResume.objects.get(user=self.request.user)
            if not resume.resume:
                return None
            if resume.resume.path.endswith('.doc'):
                text = textract.process(resume.resume.path).decode('utf-8')
                return text
            return None
        except ObjectDoesNotExist:
            print("Resume file does not exist for the user.")
            return None
        except Exception as e:
            print(f"An error occurred while extracting text from DOC: {e}")
            return None