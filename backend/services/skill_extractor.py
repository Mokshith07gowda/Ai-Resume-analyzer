# Comprehensive list of skills to detect
SKILLS_LIST = [
    # Programming Languages
    "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin",
    "Go", "Rust", "TypeScript", "Scala", "R", "MATLAB", "Perl", "C", "Dart",
    "Objective-C", "Shell", "PowerShell", "Bash", "VBA",
    
    # Web Technologies
    "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js",
    "Django", "Flask", "FastAPI", "Spring Boot", "ASP.NET", "jQuery", "Next.js",
    "Svelte", "Bootstrap", "Tailwind CSS", "SASS", "LESS", "Webpack", "Vite",
    
    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQLite", "Redis",
    "Cassandra", "DynamoDB", "Firebase", "MariaDB", "Neo4j", "Elasticsearch",
    "CouchDB", "MS SQL Server",
    
    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes", "Jenkins",
    "CI/CD", "Git", "GitHub", "GitLab", "Terraform", "Ansible", "Chef", "Puppet",
    "CircleCI", "Travis CI", "Bitbucket", "Heroku", "Netlify", "Vercel",
    
    # Data Science & AI
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras",
    "Scikit-learn", "Pandas", "NumPy", "Data Analysis", "NLP", "Computer Vision",
    "OpenCV", "NLTK", "spaCy", "Matplotlib", "Seaborn", "Plotly", "Jupyter",
    "Apache Spark", "Hadoop", "Data Mining", "Statistical Analysis",
    
    # Mobile Development
    "React Native", "Flutter", "iOS", "Android", "Xamarin", "Ionic",
    
    # Testing & QA
    "Selenium", "Jest", "Mocha", "Chai", "Pytest", "JUnit", "TestNG",
    "Cypress", "Postman", "JMeter",
    
    # Other Technologies & Skills
    "REST API", "GraphQL", "Microservices", "Agile", "Scrum", "JIRA",
    "Linux", "Windows", "macOS", "Blockchain", "IoT", "Arduino", "Raspberry Pi",
    "OAuth", "JWT", "API Development", "Web Services", "SOAP", "XML", "JSON",
    "Figma", "Adobe XD", "Photoshop", "UI/UX", "Responsive Design",
    "Version Control", "Problem Solving", "Team Collaboration", "Communication",
    "Leadership", "Project Management", "Agile Methodologies", "Data Structures",
    "Algorithms", "System Design", "OOP", "Functional Programming"
]


def extract_skills(text: str) -> list:
    """
    Extract skills from text by matching against the skills list.
    
    Args:
        text: Input text (resume or job description)
        
    Returns:
        List of detected skills
    """
    found_skills = []
    text_lower = text.lower()
    
    for skill in SKILLS_LIST:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills


def get_all_skills() -> list:
    """
    Return the complete list of available skills.
    
    Returns:
        Complete skills list
    """
    return SKILLS_LIST
