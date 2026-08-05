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

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"],
)


@router.post("/classification")
def classify(request: ClassificationRequest):

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

    result = publication_service.predict(request)

    return success_response(
        data=result,
        message="Publication prediction completed",
    )


@router.post("/recommendation")
def recommendation(request: RecommendationRequest):

    result = recommendation_service.recommend(
        request.query,
        request.top_k,
    )

    return success_response(
        data=result,
        message="Recommendations generated",
    )


@router.post("/chat")
def chat(request: MLChatRequest):

    result = ml_chat_service.chat(
        request.question,
        request.provider,
        request.api_key,
    )

    return success_response(
        data=result,
        message="Response generated",
    )