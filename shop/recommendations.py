# recommendations.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from shop.models import Product

def calculate_item_similarity(viewed_product):
    # Get all products except the viewed product
    all_products = Product.objects.exclude(id=viewed_product.id)

    # Extract descriptions for all products
    product_descriptions = [product.description for product in all_products]

    # Add the viewed product description to the list
    product_descriptions.append(viewed_product.description)

    # Initialize a TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words='english')

    # Fit and transform descriptions to TF-IDF matrix
    tfidf_matrix = tfidf.fit_transform(product_descriptions)

    # Calculate cosine similarity between products
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Get indices of all products except the last one (which is the viewed product)
    indices = range(len(all_products))

    # Get similarity scores for the viewed product with all other products
    sim_scores = list(enumerate(cosine_sim[-1][:-1]))

    # Sort products based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get indices of top similar products
    top_indices = [i for i, _ in sim_scores[:5]]  # Choose top 5 similar products

    # Return the top recommended products (excluding the viewed product)
    recommended_products = [all_products[i] for i in top_indices]

    return recommended_products
