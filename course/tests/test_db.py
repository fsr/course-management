from django.test import TestCase

from course.models.course import Course
from course.models.subject import Subject
from user.models import UserInformation
from django.contrib.auth.models import User


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


class CascadingDeletionTests(TestCase):
    """
    Test Cases to verify that cascading deletion works as expected.
    (e.g. Deleting a subject deletes all associated courses and so on...)
    """
    def test_remove_subject_that_contains_a_course(self):
        """
        Remove a subject with one course.
        Expected result: The course is being deleted.
        """
        flush_tables()
        insert_dummy_data()

        self.assertEqual(Subject.objects.count(), 1)
        self.assertEqual(Course.objects.count(), 1)

        Subject.objects.get(name='Hacking for Beginners').delete()

        self.assertEqual(Subject.objects.count(), 0, "The subject was not deleted.")
        self.assertEqual(Course.objects.count(), 0, "Course has not been removed via cascading delete!")
        self.assertEqual(UserInformation.objects.count(), 1,
                         "User is not in the database anymore, perhaps cascading deletion broke?")

    def test_remove_user_who_is_teacher_test(self):
        """
        Test Case to verify that a teacher reference is being removed from a course when the user is deleted.
        """
        flush_tables()
        insert_dummy_data()

        self.assertEqual(UserInformation.objects.count(), 1, 'No user was created!')
        self.assertEqual(Course.objects.count(), 1, 'No course was created!')

        User.objects.get(username='hfinch').delete()

        c = Course.objects.get(subject=Subject.objects.get(name='Hacking for Beginners'))

        self.assertEqual(UserInformation.objects.count(), 0, 'The user has not been removed!')
        self.assertEqual(c.teacher.count(), 0, 'The teacher reference still exists although the user was removed.')

