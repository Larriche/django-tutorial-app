# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from .models import Course
from .models import Step

class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title='Python Regular Expressions',
            description='Learn to write regular expressions in Python'
        )
        now = timezone.now()

        self.course = course

        self.assertLess(course.created_at, now)

    def test_step_creation(self):
        course = Course.objects.create(
            title='Python Unit Testing',
            description='Learn to write unit tests in Python'
        )

        step = Step.objects.create(
            title='Learn Docstrings',
            description='Learn to write tests in docstrings',
            course=course
        )

        self.assertIn(step, course.step_set.all())

class CourseViewsTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='Python Testing',
            description='Learn to write tests in Python'
        )

        self.course2 = Course.objects.create(
            title='Unit Testing In Django',
            description='Unit testing in Python'
        )

        self.step = Step.objects.create(
            title='Introduction to Doctests',
            description='Learn to write tests in your docstrings',
            course=self.course
        )

    def test_course_list_view(self):
        response = self.client.get(reverse('courses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.course, response.context['courses'])
        self.assertIn(self.course2, response.context['courses'])
        self.assertTemplateUsed(response, 'courses/course_list.html')
        self.assertContains(response, self.course.title)

    def test_course_detail_view(self):
        response = self.client.get(reverse('courses:detail', kwargs={'pk': self.course.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.course.title, response.context['course'].title)
        self.assertTemplateUsed(response, 'courses/course_detail.html')
        self.assertContains(response, self.course.title)

    def test_step_detail_view(self):
        response = self.client.get(reverse('courses:step', kwargs={'course_pk': self.course.id,
            'step_pk': self.step.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.step.title, response.context['step'].title)
        self.assertTemplateUsed(response, 'courses/step_detail.html')
        self.assertContains(response, self.step.title)
