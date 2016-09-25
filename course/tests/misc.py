from course.models.course import Course
from course.models.subject import Subject
from user.models import UserInformation


def flush_tables():
    Subject.objects.all().delete()
    Course.objects.all().delete()
    UserInformation.objects.all().delete()


def insert_dummy_data():
    u1 = UserInformation.create('hfinch', 'harold.finch@ift.web', 'test', 'Harold', 'Finch')
    u1.user.is_active = True
    u1.user.save()

    s1 = Subject.objects.create(
        name='Hacking for Beginners',
        description='Nothing to see here.'
    )
    s1.save()

    c1 = Course.objects.create(
        subject=s1,
        max_participants=1,
    )
    c1.teacher.add(u1)
    c1.save()
