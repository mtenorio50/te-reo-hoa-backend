import random
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import auth, models, schemas, crud
from app.database import get_db


logger = logging.getLogger(__name__)
router = APIRouter(tags=["Quiz"])
user_quiz_sessions = {}


@router.get("/next", response_model=schemas.QuizQuestion)
def get_quiz_question(
    db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)
):
    stats = crud.get_user_progress_stats(db, current_user.id)
    if stats["learned_count"] < 10:
        needed = 10 - stats["learned_count"]
        raise HTTPException(
            status_code=403,
            detail=f"You need to learn at least 10 words before taking the quiz. Learn {needed} more words first."
        )

    learned_words = crud.get_learned_words_for_user(db, current_user.id)
    if len(learned_words) < 4:
        raise HTTPException(
            status_code=400,
            detail="You need at least 4 learned words to take the quiz."
        )

    correct_word = random.choice(learned_words)
    correct_translation = correct_word.translation
    decoys = random.sample([w for w in learned_words if w.id != correct_word.id], 3)
    choices = [w.translation for w in decoys] + [correct_translation]
    random.shuffle(choices)
    correct_index = choices.index(correct_translation)

    # Store choices in session
    user_quiz_sessions[(current_user.id, correct_word.id)] = choices

    return schemas.QuizQuestion(
        word_id=correct_word.id,
        question=f"What is the Māori translation for '{correct_word.text}'?",
        choices=choices,
        correct_index=correct_index
    )

@router.post("/answer", response_model=schemas.QuizResult)
def submit_quiz_answer(
    answer: schemas.QuizAnswerSubmission,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    session_key = (current_user.id, answer.word_id)
    if session_key not in user_quiz_sessions:
        raise HTTPException(status_code=400, detail="Quiz session not found or expired.")

    choices = user_quiz_sessions[session_key]
    if answer.chosen_index < 0 or answer.chosen_index >= len(choices):
        raise HTTPException(status_code=400, detail="Invalid choice index.")

    word = db.query(models.Word).filter_by(id=answer.word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found.")

    is_correct = choices[answer.chosen_index].strip().lower() == word.translation.strip().lower()
    del user_quiz_sessions[session_key]  # Optionally remove session after answer

    return schemas.QuizResult(correct=is_correct)
