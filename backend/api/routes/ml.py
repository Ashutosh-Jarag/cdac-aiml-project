"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the machine learning (ML) API router module for the FastAPI application.
It exposes HTTP endpoints under the "/ml" prefix for various machine learning operations, including:
  1. Classification: Predicting categories or labels from text titles and abstracts.
  2. Publication Prediction: Evaluating publication-related metrics or statuses from input payloads.
  3. Recommendation Systems: Generating recommendations based on a given title, abstract, and count limit.
  4. ML Chat: Handling machine learning conversational tasks via specified LLM providers and API keys.
"""

from fastapi import APIRouter

from app.middleware.response import success_response

from api.schemas.ml import (
    ClassificationRequest,
    PublicationRequest,
    RecommendationRequest,
    MLChatRequest,
)

from services.ml.classification_service import classification_service
from services.ml.publication_service import publication_service
from services.ml.recommendation_service import recommendation_service
from services.ml.chat_service import ml_chat_service

# Initialize the Machine Learning router with a prefix and OpenAPI tags
router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"],
)


@router.post("/classification")
def classify(request: ClassificationRequest):
    """
    Performs text classification using the provided title and abstract.

    Args:
        request (ClassificationRequest): Request body containing the text 'title' and 'abstract'.

    Returns:
        dict: Standardized success response containing classification prediction results and message.
    """
    result = classification_service.predict(
        request.title,
        request.abstract,
    )

    return success_response(
        data=result,
        message="Classification completed",
    )


@router.post("/publication")
def publication(request: PublicationRequest):
    """
    Evaluates and predicts publication outcomes based on the provided request payload.

    Args:
        request (PublicationRequest): Request body containing data attributes required for publication prediction.

    Returns:
        dict: Standardized success response containing publication prediction results and message.
    """
    result = publication_service.predict(request)

    return success_response(
        data=result,
        message="Publication prediction completed",
    )


@router.post("/recommendation")
def recommendation(request: RecommendationRequest):
    """
    Generates item or text recommendations using a given title, abstract, and top_k threshold.

    Args:
        request (RecommendationRequest): Request body containing 'title', 'abstract', and 'top_k' parameters.

    Returns:
        dict: Standardized success response containing the generated recommendations and message.
    """
    result = recommendation_service.recommend(
        request.title,
        request.abstract,
        request.top_k,
    )

    return success_response(
        data=result,
        message="Recommendations generated",
    )


@router.post("/chat")
def chat(request: MLChatRequest):
    """
    Processes machine learning chat inquiries using a specified conversational service provider.

    Args:
        request (MLChatRequest): Request body containing the user's 'question', optional 'provider', and 'api_key'.

    Returns:
        dict: Standardized success response containing the generated AI response and message.
    """
    result = ml_chat_service.chat(
        request.question,
        request.provider,
        request.api_key,
    )

    return success_response(
        data=result,
        message="Response generated",
    )