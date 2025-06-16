from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, auth
from app.database import get_db
import random

router = APIRouter(tags=["Quiz"])

@router.get("/next", response_model=schemas.QuizQuestion)
def get_quiz_question(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    words = db.query(models.Word).all()
    if len(words) < 4:
        raise HTTPException(status_code=400, detail="Not enough words for a quiz.")
    correct_word = random.choice(words)
    correct_translation = correct_word.translation
    decoy_words = [w for w in words if w.id != correct_word.id]
    decoys = random.sample(decoy_words, 3)
    choices = [w.translation for w in decoys] + [correct_translation]
    random.shuffle(choices)
    correct_index = choices.index(correct_translation)
    return schemas.QuizQuestion(
        word_id=correct_word.id,
        question=f"What is the Māori translation for '{correct_word.text}'?",
        choices=choices,
        correct_index=correct_index,
    )

@router.post("/answer", response_model=schemas.QuizResult)
def submit_quiz_answer(
    answer: schemas.QuizAnswerSubmission,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    word = db.query(models.Word).filter_by(id=answer.word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found.")
    words = db.query(models.Word).filter(models.Word.id != word.id).all()
    if len(words) < 3:
        raise HTTPException(status_code=400, detail="Not enough words for decoys.")
    decoys = random.sample(words, 3)
    choices = [w.translation for w in decoys] + [word.translation]
    random.shuffle(choices)
    correct_index = choices.index(word.translation)
    is_correct = (answer.chosen_index == correct_index)
    return schemas.QuizResult(
        correct=is_correct,
        correct_answer=word.translation
    )