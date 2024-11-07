import random
from datetime import datetime

from datacenter.models import Schoolkid, Mark, Chastisement, Commendation,Lesson
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def improve_grades(name):
    """Функция для улучшения плохих оценок"""
    try:
        student = Schoolkid.objects.get(full_name__icontains=name)
        marks = Mark.objects.filter(schoolkid=student)

        for mark in marks:
            if mark.points < 4:
                mark.points = 4
                mark.save()

    except ObjectDoesNotExist:
        return f"Ученик с именем '{name}' не найден."
    except MultipleObjectsReturned:
        return f"Найдено несколько учеников с именем '{name}'. Уточните имя."


def delete_all_chastisements(name):
    """Функция для удаления замечаний"""
    Chastisement.objects.get(
        schoolkid__full_name__icontains=name).delete()


def create_commendation(student_name, subject_title):
    """Функция для создания похвал"""

    try:
        student = Schoolkid.objects.get(full_name__icontains=student_name)
    except ObjectDoesNotExist:
        return f"Ученик с именем '{student_name}' не найден."

    except MultipleObjectsReturned:
        return f"Найдено несколько учеников с именем '{student_name}'. Уточните имя."

    try:
        subject = Subject.objects.get(
            title=subject_title, year_of_study=student.year_of_study)
    except ObjectDoesNotExist:
        return f"Предмет '{subject_title}' не найден для ученика."

    except MultipleObjectsReturned:
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
