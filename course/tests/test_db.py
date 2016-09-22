from django.test import TestCase

from course.models.course import Course
from course.models.subject import Subject
from user.models import UserInformation
from django.contrib.auth.models import User


def flush_tables():
    Subject.objects.all().delete()
    Course.objects.all().delete()
    UserInformation.objects.all().delete()


class CheckCascadingDeletionTest(TestCase):
    """
    Test Case to verify that cascading deletion works as expected.
    (means: Deleting a subject deletes all associated courses and so on...)
    """
    def setUp(self):
        # Flush db. Just in case.
        flush_tables()

        # create a user that's gonna pose as teacher
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

    def test_db(self):
        self.assertEqual(Subject.objects.count(), 1)
        self.assertEqual(Course.objects.count(), 1)

        s = Subject.objects.get(name='Hacking for Beginners')
        s.delete()
        s.save()

        self.assertEqual(Course.objects.count(), 0, "Course has not been removed via cascading delete!")
        self.assertEqual(UserInformation.objects.count(), 1,
                         "User is not in the database anymore, perhaps cascading deletion broke?")

    def tearDown(self):
        flush_tables()


class RemoveTeacherTest(TestCase):
    """
    Test Case to verify that a teacher reference is being removec from a course when the user is deleted.
    """
    def setUp(self):
        # Flush db. Just in case.
        flush_tables()

        # create a user that's gonna pose as teacher
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

    def test_db(self):
        self.assertEqual(UserInformation.objects.count(), 1, 'No user was created!')
        self.assertEqual(Course.objects.count(), 1, 'No course was created!')

        User.objects.get(username='hfinch').delete()

        c = Course.objects.get(subject=Subject.objects.get(name='Hacking for Beginners'))

        self.assertEqual(UserInformation.objects.count(), 0, 'The user has not been removed!')
        self.assertEqual(c.teacher.count(), 0, 'The teacher reference still exists!')

    def tearDown(self):
        flush_tables()
