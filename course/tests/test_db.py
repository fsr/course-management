from django.test import TestCase

from course.models.course import Course
from course.models.subject import Subject
from user.models import UserInformation, Faculty
from django.contrib.auth.models import User

from .misc import *


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

    def test_remove_enrolled_user(self):
        """
        Verify that deleting a user who is enrolled for a course removes the enrollment.
        """
        flush_tables()
        insert_dummy_data()
        u2 = UserInformation.create('samgroves', 'samantha.groves@mail.web', 'L33T', 'Samantha', 'Groves')
        u2.user.is_active = True
        u2.user.save()

        course = Course.objects.get(subject=Subject.objects.get(name='Hacking for Beginners'))
        course.active = True
        course.save()
        course.enroll(u2)

        self.assertEqual(course.participants.count(), 1, 'There was more than one person enrolled to the course!')
        self.assertEqual(UserInformation.objects.count(), 2, 'Too much users!')

        User.objects.get(username='samgroves').delete()

        self.assertEqual(UserInformation.objects.count(), 1, "The user was not removed!")
        self.assertEqual(course.participants.count(), 0, 'There was more than one person enrolled to the course!')

    def test_only_students_can_enroll(self):
        """
        Verify that only students can enroll for a 'student-only' marked course.
        """
        flush_tables()
        insert_dummy_data()

        course = Course.objects.get(subject=Subject.objects.get(name='Hacking for Beginners'))
        course.student_only = True
        course.active = True
        course.save()

        fac = Faculty.objects.create(name="Faculty of Computer Science")
        fac.save()

        u2 = UserInformation.create('samgroves', 'samantha.groves@mail.web', 'L33T', 'Samantha', 'Groves')
        u2.user.is_active = True
        u2.user.save()
        u3 = UserInformation.create('sameen', 'sameen.shaw@mail.web', 'Sh00T', 'Sameen', 'Shaw', 's9283457', fac.pk)
        u3.user.is_active = True
        u3.user.save()

        with self.assertRaises(Course.IsNoStudent):
            course.enroll(u2)

        course.enroll(u3)

        self.assertEqual(course.participants.count(), 1,
                         'More than one participant found, although only one was registered.')



