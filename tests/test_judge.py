import pytest
from backend.app.agent.state import StudentProfile
from backend.app.agent.judge import audit_phase_logic

def test_judge_gatekeeping_incomplete():
    """Verifica che con dati insufficienti il Giudice non permetta il passaggio alla Fase 2"""
    # Profilo con solo la città (secondo i nostri prompt vale 30%)
    profilo = StudentProfile(residenza_citta="Milano")
    
    report = audit_phase_logic(profilo.model_dump(), phase=1)
    
    print(f"\n[AUDIT INCOMPLETO]: Percentuale {report.percentage}% - Can move: {report.can_move_to_next}")
    
    # Ci aspettiamo che non dia il via libera (soglia 80%)
    assert report.percentage < 80
    assert report.can_move_to_next is False

def test_judge_gatekeeping_complete():
    """Verifica che con Indirizzo Studio, Città e Aspirazioni si passi alla Fase 2"""
    # Profilo completo per la Fase 1
    profilo = StudentProfile(
        indirizzo_studio="Meccanica",
        residenza_citta="Torino",
        aspirazioni="Lavorare in Formula 1"
    )
    
    report = audit_phase_logic(profilo.model_dump(), phase=1)
    
    print(f"\n[AUDIT COMPLETO]: Percentuale {report.percentage}% - Can move: {report.can_move_to_next}")
    
    # Ci aspettiamo l'OK (40% + 30% + 30% = 100%)
    assert report.percentage >= 80
    assert report.can_move_to_next is True
