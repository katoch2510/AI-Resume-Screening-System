from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, job_description):
    """
    Calculates similarity percentage between resume and job description using TF-IDF and Cosine Similarity.
    """
    if not resume_text or not job_description:
        return 0.0
    
    documents = [resume_text, job_description]
    
    # Create TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Calculate Cosine Similarity
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    # Return percentage
    score = round(similarity_matrix[0][0] * 100, 2)
    return score

def rank_candidates(match_results):
    """
    Sorts candidates based on their match scores.
    """
    return sorted(match_results, key=lambda x: x['score'], reverse=True)
