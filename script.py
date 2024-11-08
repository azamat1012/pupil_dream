from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson, Subject
import random

def get_student_by_name(name):
    """Получение объекта школьника по имени."""
    try:
        return Schoolkid.objects.get(full_name__icontains=name)
    except Schoolkid.DoesNotExist:
        raise Schoolkid.DoesNotExist(f"Ученик с именем '{name}' не найден.")
    except Schoolkid.MultipleObjectsReturned:
        raise Schoolkid.MultipleObjectsReturned(f"Найдено несколько учеников с именем '{name}'. Уточните имя.")

def improve_grades(name):
    """Функция для массового улучшения плохих оценок."""
    student = get_student_by_name(name)
    if isinstance(student, str):
        return student  
    updated_count = Mark.objects.filter(schoolkid=student, points__lt=4).update(points=4)

def delete_all_chastisements(name):
    """Функция для удаления замечаний."""
    student = get_student_by_name(name)
    if isinstance(student, str):
        return student 
    
    Chastisement.objects.filter(schoolkid=student).delete()

def create_commendation(student_name, subject_title):
    """Функция для создания похвал."""
    student = get_student_by_name(student_name)
    if isinstance(student, str):
        return student 
    
    try:
        subject = Subject.objects.get(
            title=subject_title, year_of_study=student.year_of_study
        )
     except Subject.ObjectDoesNotExist:
        return f"Предмет '{subject_title}' не найден для ученика."
    except Subject.MultipleObjectsReturned:
        return f"Найдено несколько записей для предмета '{subject_title}'. Уточните запрос."
    
    last_lesson = Lesson.objects.filter(
        year_of_study=student.year_of_study,
        group_letter=student.group_letter,
        subject=subject
    ).order_by('-date').first()

    if not last_lesson:
        return "Занятие по данному предмету не найдено."
    
    commendations = [
        "Молодец!", "Отлично!", "Ты сделал это!", "Горжусь тобой!",
        "Продолжай в том же духе!", "Ты на верном пути!"
    ]

    Commendation.objects.create(
        text=random.choice(commendations),
        created=last_lesson.date,
        schoolkid=student,
        subject=subject,
        teacher=last_lesson.teacher
    )

    
